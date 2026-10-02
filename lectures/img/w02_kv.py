"""Week 2 — prefill vs decode, and the KV cache, for real.

Times GPT-2 on this machine (CPU): reading a 512-token prompt in one pass (prefill) vs writing 512
tokens one at a time (decode), with and without the KV cache. Then the KV-cache memory of GPT-2 and
of gpt-oss-120b at full context, from the model card's numbers (36 layers alternating dense and
128-token window, 8 key-value heads of 64, 131,072 tokens), with and without GQA. Writes w02_kv.json.
Run with ~/.venvs/ese-ai-ml.
"""
import json, time
from pathlib import Path
import torch
from transformers import GPT2LMHeadModel

HERE = Path(__file__).parent
torch.manual_seed(0)
torch.set_num_threads(4)
m = GPT2LMHeadModel.from_pretrained("gpt2").eval()
N = 512
ids = torch.randint(0, 50257, (1, N))


def best(f, k=3):
    ts = []
    for _ in range(k):
        t0 = time.perf_counter(); f(); ts.append(time.perf_counter() - t0)
    return min(ts)


with torch.no_grad():
    prefill = best(lambda: m(ids))

    def decode_cached():
        out = m(ids[:, :1], use_cache=True); past = out.past_key_values
        for i in range(1, N):
            out = m(ids[:, i:i + 1], past_key_values=past, use_cache=True); past = out.past_key_values
    decode = best(decode_cached, 1)

    M = 128                                                             # without cache: re-read everything each step
    def decode_nocache():
        for i in range(1, M + 1):
            m(ids[:, :i], use_cache=False)
    nocache_128 = best(decode_nocache, 1)
    def decode_cached_128():
        out = m(ids[:, :1], use_cache=True); past = out.past_key_values
        for i in range(1, M):
            out = m(ids[:, i:i + 1], past_key_values=past, use_cache=True); past = out.past_key_values
    cached_128 = best(decode_cached_128, 1)

B = 2                                                                    # bytes per number, 16-bit
gpt2_per_token = 2 * 12 * 768 * B                                        # K and V, 12 layers, 768 wide
oss = {"layers": 36, "dense_layers": 18, "window_layers": 18, "window": 128, "kv_heads": 8, "q_heads": 64,
       "d_head": 64, "context": 131072}
per_layer_token = 2 * oss["kv_heads"] * oss["d_head"] * B               # K and V
dense = oss["dense_layers"] * oss["context"] * per_layer_token
window = oss["window_layers"] * oss["window"] * per_layer_token
no_gqa = 2 * oss["q_heads"] * oss["d_head"] * B * oss["layers"] * oss["context"]   # 64 K/V heads, all dense
out = {"machine": "laptop CPU, 4 threads, GPT-2 small", "N": N,
       "prefill_s": round(prefill, 3), "decode_cached_s": round(decode, 3),
       "prefill_tokens_per_s": round(N / prefill), "decode_tokens_per_s": round((N - 1) / decode, 1),
       "M": M, "decode_nocache_s": round(nocache_128, 2), "decode_cached_M_s": round(cached_128, 2),
       "gpt2_kv_bytes_per_token": gpt2_per_token, "gpt2_kv_full_context_MB": round(gpt2_per_token * 1024 / 1e6, 1),
       "oss": oss, "oss_kv_GB_full_context": round((dense + window) / 1e9, 2),
       "oss_kv_GB_if_no_gqa_no_window": round(no_gqa / 1e9, 1)}
(HERE / "w02_kv.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))

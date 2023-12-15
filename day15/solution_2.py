from contextlib import redirect_stdout
from pathlib import Path

INPUT_NAME = "input.txt"

def rolling_hash(text: str) -> int:
    value = 0
    for c in text:
        value = 17 * (value + ord(c)) % 256
    # print(f"{value} <- {text}")
    return value

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / INPUT_NAME

    sol = 0
    hash = {i: [] for i in range(256)}

    with open(script_dir / 'output.txt', 'w') as f:
      with redirect_stdout(f):
        with open(file_path, 'r') as file:
            lines = [line.rstrip() for line in file]
            inputs = lines[0].split(",")
            
            for instruction in inputs:
                if instruction[-1] == '-':
                    label = instruction[:-1]
                    hash_bucket_idx = rolling_hash(label)
                    idx = next((idx for idx, lens in enumerate(hash[hash_bucket_idx]) if lens[0] == label), -1)
                    if idx >= 0:
                        del hash[hash_bucket_idx][idx]
                else:
                    label, focal_length = instruction[:-2], int(instruction[-1])
                    hash_bucket_idx = rolling_hash(label)
                    idx = next((idx for idx, lens in enumerate(hash[hash_bucket_idx]) if lens[0] == label), -1)
                    if idx >= 0:
                        hash[hash_bucket_idx][idx] = (label, focal_length)
                    else:
                        hash[hash_bucket_idx].append((label, focal_length))
                
            sol = sum(
                (hash_bucket_idx + 1) * (idx + 1) * lens[1]
                for hash_bucket_idx in range(256)
                for idx, lens in enumerate(hash[hash_bucket_idx])
            )

        print(f"------> {sol}")
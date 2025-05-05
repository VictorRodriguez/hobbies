import json
import random
import math

def is_power_of_two(x):
    """Check if a number is a power of 2."""
    return x > 0 and (x & (x - 1)) == 0

def is_valid_cache(cache_size, block_size, associativity):
    """Validate cache parameters."""
    if not is_power_of_two(cache_size) or not is_power_of_two(block_size):
        return False

    num_blocks = cache_size // block_size
    if num_blocks % associativity != 0:
        return False

    num_sets = cache_size // (associativity * block_size)
    return is_power_of_two(num_sets)

def random_power_of_two(min_val, max_val):
    """Generate a random power of 2 within a range."""
    powers = [2**i for i in range(int(math.log2(min_val)), int(math.log2(max_val)) + 1)]
    return random.choice(powers)

def generate_valid_cache_configs(num_configs=5):
    """Generate a list of valid cache configurations."""
    cache_size_range = (4096, 262144)  # 4 KB to 256 KB
    block_size_range = (16, 128)  # 16 B to 128 B
    associativity_options = [1, 2, 4, 8, 16]  # Typical associativity levels

    valid_configs = []

    while len(valid_configs) < num_configs:
        cache_size = random_power_of_two(*cache_size_range)
        block_size = random_power_of_two(*block_size_range)
        associativity = random.choice(associativity_options)

        if is_valid_cache(cache_size, block_size, associativity):
            valid_configs.append({
                "cache_size": cache_size,
                "block_size": block_size,
                "associativity": associativity
            })

    return valid_configs

if __name__ == "__main__":
    configs = generate_valid_cache_configs()

    # Save to JSON file
    with open("cache_configs.json", "w") as f:
        json.dump({"valid_cache_configs": configs}, f, indent=4)

    # Print output
    print(json.dumps({"valid_cache_configs": configs}, indent=4))


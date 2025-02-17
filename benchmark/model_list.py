models = [
    "openai/gpt-4o-2024-08-06",
    "openai/gpt-4o-2024-05-13",
    "openai/gpt-4o-mini-2024-07-18",
    "openai/gpt-4-1106-preview",
    "openai/gpt-4-turbo",  # Newest Turbo
    "openai/chatgpt-4o-latest",
    "openai/o1-mini",
    "openai/o1-preview",
    "openai/o1",
    "meta-llama/llama-3.1-8b-instruct",
    "meta-llama/llama-3.1-70b-instruct",
    "meta-llama/llama-3.1-405b-instruct",
    "meta-llama/llama-3.1-405b-instruct:bf16",
    "meta-llama/llama-3.2-3b-instruct",
    "meta-llama/llama-3.2-1b-instruct",
    "meta-llama/llama-3.2-90b-vision-instruct",
    "meta-llama/llama-3.2-11b-vision-instruct",
    "meta-llama/llama-3.3-70b-instruct",
    "anthropic/claude-3-5-haiku-20241022",
    "anthropic/claude-3.5-sonnet",  # New Sonnet
    "anthropic/claude-3.5-sonnet-20240620",  # Old Sonnet
    "anthropic/claude-3-sonnet",
    "anthropic/claude-3-opus",
    "anthropic/claude-3-haiku",
    "google/gemini-flash-1.5-8b",
    "google/gemini-flash-1.5",
    "google/gemini-pro-1.5",
    "google/gemma-2-27b-it",
    "google/gemma-2-9b-it",
    "google/gemini-2.0-flash-exp",
    "google/gemini-2.0-flash-thinking-exp-1219",
    "google/gemini-exp-1206",
    "x-ai/grok-beta",
    "mistralai/mixtral-8x22b-instruct",
    "mistralai/mistral-large-latest",
    "mistralai/mistral-7b-instruct-v0.3",
    "deepseek/deepseek-chat"
]

model_prices = [
    {'model': 'openai/gpt-4o-2024-08-06', 'input_price': 2.5, 'output_price': 10},   
    {'model': 'openai/gpt-4o-2024-05-13', 'input_price': 5, 'output_price': 15},
    {'model': 'openai/gpt-4o-mini-2024-07-18', 'input_price': 0.15, 'output_price': 0.6},
    {'model': 'openai/gpt-4-0314', 'input_price': 30, 'output_price': 60},
    {'model': 'openai/gpt-4-1106-preview', 'input_price': 10, 'output_price': 30},
    {'model': 'openai/gpt-4-turbo', 'input_price': 10, 'output_price': 30},
    {'model': 'openai/o1-mini', 'input_price': 3, 'output_price': 12},
    {'model': 'openai/o1-preview', 'input_price': 15, 'output_price': 60},
    {'model': 'meta-llama/llama-3.1-8b-instruct', 'input_price': 0.05, 'output_price': 0.05},
    {'model': 'meta-llama/llama-3.1-70b-instruct', 'input_price': 0.34, 'output_price': 0.39},
    {'model': 'meta-llama/llama-3.1-405b-instruct', 'input_price': 2.75, 'output_price': 2.75},
    {'model': 'meta-llama/llama-3.1-405b-instruct:bf16', 'input_price': 3, 'output_price': 3},
    {'model': 'meta-llama/llama-3.2-3b-instruct', 'input_price': 0.03, 'output_price': 0.05},
    {'model': 'meta-llama/llama-3.2-1b-instruct', 'input_price': 0.01, 'output_price': 0.02},
    {'model': 'meta-llama/llama-3.2-90b-vision-instruct', 'input_price': 0.9, 'output_price': 0.9},
    {'model': 'meta-llama/llama-3.2-11b-vision-instruct', 'input_price': 0.055, 'output_price': 0.055},
    {'model': 'anthropic/claude-3-5-haiku-20241022', 'input_price': 1, 'output_price': 5},
    {'model': 'anthropic/claude-3.5-sonnet', 'input_price': 3, 'output_price': 15},
    {'model': 'anthropic/claude-3.5-sonnet-20240620', 'input_price': 3, 'output_price': 15},
    {'model': 'anthropic/claude-3-sonnet', 'input_price': 3, 'output_price': 15},
    {'model': 'anthropic/claude-3-opus', 'input_price': 15, 'output_price': 75},
    {'model': 'anthropic/claude-3-haiku', 'input_price': 0.25, 'output_price': 1.25},
    {'model': 'google/gemini-flash-1.5-8b', 'input_price': 0.0375, 'output_price': 0.15},
    {'model': 'google/gemini-flash-1.5-pro', 'input_price': 0.075, 'output_price': 0.3},
    {'model': 'google/gemini-pro-1.5', 'input_price': 1.25, 'output_price': 5},
    {'model': 'google/gemma-2-27b-it', 'input_price': 0.27, 'output_price': 0.27},
    {'model': 'google/gemma-2-9b-it', 'input_price': 0.06, 'output_price': 0.06},
    {'model': 'x-ai/grok-beta', 'input_price': 5, 'output_price': 15},
    {'model': 'mistralai/mixtral-8x22b-instruct', 'input_price': 0.9, 'output_price': 0.9},
    {'model': 'mistralai/mistral-large-latest', 'input_price': 2, 'output_price': 6},
    {'model': 'mistralai/mistral-7b-instruct-v0.3', 'input_price': 0.055, 'output_price': 0.055},
]

lmsys_scores = [
        {'model': 'openai/gpt-4o-2024-08-06', 'lmsys_score': 1265},
        {'model': 'openai/gpt-4o-2024-05-13', 'lmsys_score': 1285},
        {'model': 'openai/gpt-4o-mini-2024-07-18', 'lmsys_score': 1272},
        {'model': 'openai/gpt-4-0314', 'lmsys_score': 1186}, # deprecated
        {'model': 'openai/gpt-4-1106-preview', 'lmsys_score': 1250}, # deprecated
        {'model': 'openai/gpt-4-turbo', 'lmsys_score': 1256}, # deprecated
        {'model': 'openai/o1-mini', 'lmsys_score': 1308},
        {'model': 'openai/o1-preview', 'lmsys_score': 1333},
        {'model': 'meta-llama/llama-3.1-8b-instruct', 'lmsys_score': 1175},
        {'model': 'meta-llama/llama-3.1-70b-instruct', 'lmsys_score': 1247},
        {'model': 'meta-llama/llama-3.1-405b-instruct', 'lmsys_score': 1267},
        {'model': 'meta-llama/llama-3.1-405b-instruct:bf16', 'lmsys_score': 1266},
        {'model': 'meta-llama/llama-3.2-3b-instruct', 'lmsys_score': 1103},
        {'model': 'meta-llama/llama-3.2-1b-instruct', 'lmsys_score': 1053},
        # {'model': 'meta-llama/llama-3.2-90b-vision-instruct', 'lmsys_score': 0.5},
        # {'model': 'meta-llama/llama-3.2-11b-vision-instruct', 'lmsys_score': 0.5},
        # {'model': 'anthropic/claude-3-5-haiku-20241022', 'lmsys_score': 0.5},
        {'model': 'anthropic/claude-3.5-sonnet', 'lmsys_score': 1283},
        {'model': 'anthropic/claude-3.5-sonnet-20240620', 'lmsys_score': 1268},
        {'model': 'anthropic/claude-3-sonnet', 'lmsys_score': 1201},
        {'model': 'anthropic/claude-3-opus', 'lmsys_score': 1248},
        {'model': 'anthropic/claude-3-haiku', 'lmsys_score': 1179},
        {'model': 'google/gemini-flash-1.5-8b', 'lmsys_score': 1211},
        {'model': 'google/gemini-flash-1.5-pro', 'lmsys_score': 1227},
        {'model': 'google/gemini-pro-1.5', 'lmsys_score': 1301},
        {'model': 'google/gemma-2-27b-it', 'lmsys_score': 1219},
        {'model': 'google/gemma-2-9b-it', 'lmsys_score': 1190},
        {'model': 'x-ai/grok-beta', 'lmsys_score': 1290},
        {'model': 'mistralai/mixtral-8x22b-instruct', 'lmsys_score': 1148},
        {'model': 'mistralai/mistral-large-latest', 'lmsys_score': 1251},
        # {'model': 'mistralai/mistral-7b-instruct-v0.3', 'lmsys_score': 0.5},
]

release_dates = [
    {'model': 'openai/gpt-4o-2024-08-06', 'release_date': '2024-08-06'},
    {'model': 'openai/gpt-4o-2024-05-13', 'release_date': '2024-05-13'},
    {'model': 'openai/gpt-4o-mini-2024-07-18', 'release_date': '2024-07-18'},
    {'model': 'openai/gpt-4-0314', 'release_date': '2023-03-14'},
    {'model': 'openai/gpt-4-1106-preview', 'release_date': '2023-11-06'},
    {'model': 'openai/gpt-4-turbo', 'release_date': '2024-05-10'},
    {'model': 'openai/o1-mini', 'release_date': '2024-09-12'},
    {'model': 'openai/o1-preview', 'release_date': '2024-09-12'},
    {'model': 'meta-llama/llama-3.1-8b-instruct', 'release_date': '2024-07-23'},
    {'model': 'meta-llama/llama-3.1-70b-instruct', 'release_date': '2024-07-23'},
    {'model': 'meta-llama/llama-3.1-405b-instruct', 'release_date': '2024-07-23'},
    {'model': 'meta-llama/llama-3.1-405b-instruct:bf16', 'release_date': '2024-07-23'},
    {'model': 'meta-llama/llama-3.2-3b-instruct', 'release_date': '2024-09-25'},
    {'model': 'meta-llama/llama-3.2-1b-instruct', 'release_date': '2024-09-25'},
    {'model': 'meta-llama/llama-3.2-90b-vision-instruct', 'release_date': '2024-09-25'},
    {'model': 'meta-llama/llama-3.2-11b-vision-instruct', 'release_date': '2024-09-25'},
    {'model': 'anthropic/claude-3-5-haiku-20241022', 'release_date': '2024-10-22'},
    {'model': 'anthropic/claude-3.5-sonnet', 'release_date': '2024-10-22'},
    {'model': 'anthropic/claude-3.5-sonnet-20240620', 'release_date': '2024-06-20'},
    {'model': 'anthropic/claude-3-sonnet', 'release_date': '2024-03-04'},
    {'model': 'anthropic/claude-3-opus', 'release_date': '2024-03-04'},
    {'model': 'anthropic/claude-3-haiku', 'release_date': '2024-03-04'},
    {'model': 'google/gemini-flash-1.5-8b', 'release_date': '2024-10-03'},
    {'model': 'google/gemini-flash-1.5-pro', 'release_date': '2024-09-24'},
    {'model': 'google/gemini-pro-1.5', 'release_date': '2024-09-24'},
    {'model': 'google/gemma-2-27b-it', 'release_date': '2024-06-27'},
    {'model': 'google/gemma-2-9b-it', 'release_date': '2024-06-27'},
    {'model': 'x-ai/grok-beta', 'release_date': '2024-08-14'},
    {'model': 'mistralai/mixtral-8x22b-instruct', 'release_date': '2024-04-17'},
    {'model': 'mistralai/mistral-large-latest', 'release_date': '2024-07-18'},
    {'model': 'mistralai/mistral-7b-instruct-v0.3', 'release_date': '2024-05-24'},
]

model_scales = [
    {'model': 'openai/gpt-4-0314', 'parameters': 1.8e12},
    {'model': 'meta-llama/llama-3.1-8b-instruct', 'parameters': 8e9},
    {'model': 'meta-llama/llama-3.1-70b-instruct', 'parameters': 7e10},
    {'model': 'meta-llama/llama-3.1-405b-instruct', 'parameters': 4.05e11},
    {'model': 'meta-llama/llama-3.1-405b-instruct:bf16', 'parameters': 4.05e11},
    {'model': 'meta-llama/llama-3.2-3b-instruct', 'parameters': 3e9},
    {'model': 'meta-llama/llama-3.2-1b-instruct', 'parameters': 1e9},
    {'model': 'meta-llama/llama-3.2-90b-vision-instruct', 'parameters': 9e10},
    {'model': 'meta-llama/llama-3.2-11b-vision-instruct', 'parameters': 1.1e10},
    {'model': 'google/gemini-flash-1.5-8b', 'parameters': 8e9},
    {'model': 'google/gemma-2-27b-it', 'parameters': 2.7e10},
    {'model': 'google/gemma-2-9b-it', 'parameters': 9e9},
    {'model': 'mistralai/mixtral-8x22b-instruct', 'parameters': 1.76e11},
    {'model': 'mistralai/mistral-7b-instruct-v0.3', 'parameters': 7e9},
]

model_subset = [
    "openai/gpt-4o-mini-2024-07-18",
    "meta-llama/llama-3.1-70b-instruct",
    "google/gemini-flash-1.5-8b",
    "anthropic/claude-3.5-sonnet",  # New Sonnet
    "gpt-4-turbo"
]

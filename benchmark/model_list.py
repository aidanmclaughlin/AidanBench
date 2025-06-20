models = [
    "openai/gpt-4o-2024-08-06",
    "openai/gpt-4o-2024-05-13",
    "openai/gpt-4o-mini-2024-07-18",
    "openai/gpt-4-1106-preview",
    "openai/gpt-4-turbo",  # Newest Turbo
    "openai/gpt-4.5-preview",
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
    "anthropic/claude-3.7-sonnet:thinking",
    "anthropic/claude-3.7-sonnet",
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
    "google/gemma-3-4b-it",
    "google/gemma-3-12b-it",
    "google/gemma-3-27b-it",
    "google/gemini-2.0-flash-exp",
    "google/gemini-2.0-flash-thinking-exp-1219",
    "google/gemini-2.0-flash",
    "google/gemini-2.0-flash-lite",
    "google/gemini-2.0-pro-experimental",
    "google/gemini-2.5-pro-preview-03-25",
    "x-ai/grok-beta",
    "x-ai/grok-3-beta",
    "x-ai/grok-3-mini-beta:low",
    "x-ai/grok-3-mini-beta:medium",
    "x-ai/grok-3-mini-beta:high",
    "mistralai/mixtral-8x22b-instruct",
    "mistralai/mistral-large-latest",
    "mistralai/mistral-7b-instruct-v0.3",
    "deepseek/deepseek-chat",
    "openai/o3-mini:high",
    "openai/o3-mini:medium",
    "openai/o3-mini:low",
    "openai/o3",
    "openai/o3-pro",
    "openai/o4-mini",
    "openai/gpt-4.1-nano",
    "anthropic/claude-opus-4",
    "anthropic/claude-sonnet-4",
    "anthropic/claude-opus-4:thinking",
    "anthropic/claude-sonnet-4:thinking",
    "x-ai/grok-3-beta:thinking",
    "x-ai/grok-3-mini-beta:thinking",
    "google/gemini-2.5-pro",
    "google/gemini-2.5-pro:thinking",
    "google/gemini-2.5-flash:thinking",
    "deepseek/deepseek-r1-0528",
    "mistralai/mistral-saba-25.02",
    "mistralai/mistral-small-3.1",
    "mistralai/mistral-medium-3",
    "mistralai/magistral-small",
    "mistralai/magistral-medium",
    "mistralai/devstral-small",
]

model_prices = [
    {'model': 'openai/gpt-4o-2024-08-06', 'input_price': 2.5, 'output_price': 10},
    {'model': 'openai/gpt-4o-2024-05-13', 'input_price': 5, 'output_price': 15},
    {'model': 'openai/gpt-4o-mini-2024-07-18', 'input_price': 0.15, 'output_price': 0.6},
    {'model': 'openai/gpt-4-0314', 'input_price': 30, 'output_price': 60},
    {'model': 'openai/gpt-4-1106-preview', 'input_price': 10, 'output_price': 30},
    {'model': 'openai/gpt-4-turbo', 'input_price': 10, 'output_price': 30},
    {'model': 'openai/gpt-4.5-preview', 'input_price': 75, 'output_price': 150},
    {'model': 'openai/o1-mini', 'input_price': 3, 'output_price': 12, 'reasoning_multplier': 12.0},  # o1-mini: (235-31)/17
    {'model': 'openai/o3-mini:high', 'input_price': 1.1, 'output_price': 4.4, 'reasoning_multplier': 26.823529411764707},  # o3-mini-high: (498-42)/17
    {'model': 'openai/o3-mini:medium', 'input_price': 1.1, 'output_price': 4.4, 'reasoning_multplier': 11.882352941176471},  # o3-mini-medium: (239-37)/17
    {'model': 'openai/o3-mini:low', 'input_price': 1.1, 'output_price': 4.4, 'reasoning_multplier': 4.352941176470588},  # o3-mini-low: (105-31)/17
    {'model': 'openai/o1-preview', 'input_price': 15, 'output_price': 60, 'reasoning_multplier': 21.764705882352942},  # o1-preview: (409-39)/17
    {'model': 'openai/o1', 'input_price': 15, 'output_price': 60, 'reasoning_multplier': 19.352941176470587},  # o1: (367-38)/17
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
    {'model': 'anthropic/claude-3.7-sonnet:thinking', 'input_price': 3, 'output_price': 15, 'reasoning_multplier': 19.9411}, # thinking: 339 / 17
    {'model': 'anthropic/claude-3.7-sonnet', 'input_price': 3, 'output_price': 15},
    {'model': 'anthropic/claude-3.5-sonnet-20240620', 'input_price': 3, 'output_price': 15},
    {'model': 'anthropic/claude-3-sonnet', 'input_price': 3, 'output_price': 15},
    {'model': 'anthropic/claude-3-opus', 'input_price': 15, 'output_price': 75},
    {'model': 'anthropic/claude-3-haiku', 'input_price': 0.25, 'output_price': 1.25},
    {'model': 'google/gemini-flash-1.5-8b', 'input_price': 0.0375, 'output_price': 0.15},
    {'model': 'google/gemini-flash-1.5-pro', 'input_price': 0.075, 'output_price': 0.3},
    {'model': 'google/gemini-pro-1.5', 'input_price': 1.25, 'output_price': 5},
    {'model': 'google/gemma-2-27b-it', 'input_price': 0.27, 'output_price': 0.27},
    {'model': 'google/gemma-2-9b-it', 'input_price': 0.06, 'output_price': 0.06},
    {'model': 'google/gemini-2.0-flash-exp', 'input_price': 0.1, 'output_price': 0.4},
    {'model': 'google/gemini-2.0-flash-thinking-exp-1219', 'input_price': 0.1, 'output_price': 0.4, 'reasoning_multplier': 50.52941176470588},  # 2.0 thinking: (889-30)/17
    {'model': 'google/gemini-2.0-flash', 'input_price': 0.075, 'output_price': 0.3},
    {'model': 'google/gemini-2.0-flash-lite', 'input_price': 0.05, 'output_price': 0.2},
    {'model': 'google/gemini-2.0-pro-experimental', 'input_price': 1.25, 'output_price': 5},
    {'model': 'x-ai/grok-beta', 'input_price': 5, 'output_price': 15},
    {'model': 'mistralai/mixtral-8x22b-instruct', 'input_price': 0.9, 'output_price': 0.9},
    {'model': 'mistralai/mistral-large-latest', 'input_price': 2, 'output_price': 6},
    {'model': 'mistralai/mistral-7b-instruct-v0.3', 'input_price': 0.055, 'output_price': 0.055},
    {'model': 'deepseek/deepseek-r1', 'input_price': 0.55, 'output_price': 2.59, 'reasoning_multplier': 18.88235294117647}, # r1: (354-33)/17
    {'model': 'openai/o3', 'input_price': 20, 'output_price': 80, 'reasoning_multiplier': 30.0}, # Full o3 model
    {'model': 'openai/o3-pro', 'input_price': 20, 'output_price': 80},
    {'model': 'openai/o4-mini', 'input_price': 1.1, 'output_price': 4.4},
    {'model': 'openai/gpt-4.1-nano', 'input_price': 0.5, 'output_price': 2},
    {'model': 'anthropic/claude-opus-4', 'input_price': 15, 'output_price': 75},
    {'model': 'anthropic/claude-sonnet-4', 'input_price': 3, 'output_price': 15},
    {'model': 'anthropic/claude-opus-4:thinking', 'input_price': 15, 'output_price': 75, 'reasoning_multiplier': 20.0}, # Estimate based on claude-3.7-sonnet:thinking
    {'model': 'anthropic/claude-sonnet-4:thinking', 'input_price': 3, 'output_price': 15, 'reasoning_multiplier': 20.0}, # Estimate based on claude-3.7-sonnet:thinking
    {'model': 'x-ai/grok-3-beta:thinking', 'input_price': 5, 'output_price': 15, 'reasoning_multiplier': 25.0}, # Estimate for thinking mode
    {'model': 'x-ai/grok-3-mini-beta:thinking', 'input_price': 5, 'output_price': 15, 'reasoning_multiplier': 15.0}, # Estimate for mini thinking
    {'model': 'google/gemini-2.5-pro', 'input_price': 2, 'output_price': 8},
    {'model': 'google/gemini-2.5-pro:thinking', 'input_price': 2, 'output_price': 8, 'reasoning_multiplier': 30.0},
    {'model': 'google/gemini-2.5-flash:thinking', 'input_price': 0.15, 'output_price': 0.6, 'reasoning_multiplier': 25.0},
    {'model': 'deepseek/deepseek-r1-0528', 'input_price': 0.55, 'output_price': 2.59, 'reasoning_multiplier': 25.0},
    {'model': 'mistralai/mistral-saba-25.02', 'input_price': 0.5, 'output_price': 1.5},
    {'model': 'mistralai/mistral-small-3.1', 'input_price': 0.2, 'output_price': 0.6},
    {'model': 'mistralai/mistral-medium-3', 'input_price': 1, 'output_price': 3},
    {'model': 'mistralai/magistral-small', 'input_price': 0.5, 'output_price': 1.5, 'reasoning_multiplier': 15.0},
    {'model': 'mistralai/magistral-medium', 'input_price': 2, 'output_price': 6, 'reasoning_multiplier': 20.0},
    {'model': 'mistralai/devstral-small', 'input_price': 0.3, 'output_price': 0.9}
]

lmsys_scores = [
        {'model': 'openai/gpt-4o-2024-08-06', 'lmsys_score': 1265},
        {'model': 'openai/gpt-4o-2024-05-13', 'lmsys_score': 1285},
        {'model': 'openai/gpt-4o-mini-2024-07-18', 'lmsys_score': 1272},
        {'model': 'openai/gpt-4-0314', 'lmsys_score': 1186}, # deprecated
        {'model': 'openai/gpt-4-1106-preview', 'lmsys_score': 1250}, # deprecated
        {'model': 'openai/gpt-4-turbo', 'lmsys_score': 1256}, # deprecated
        {'model': 'openai/gpt-4.5-preview', 'lmsys_score': 1411},
        {'model': 'openai/o1-mini', 'lmsys_score': 1308},
        {'model': 'openai/o1-preview', 'lmsys_score': 1333},
        {'model': 'openai/o1', 'lmsys_score': 1352},
        {'model': 'openai/o3-mini:high', 'lmsys_score': 1329},
        {'model': 'openai/o3-mini:medium', 'lmsys_score': 1304},
        {'model': 'meta-llama/llama-3.1-8b-instruct', 'lmsys_score': 1175},
        {'model': 'meta-llama/llama-3.1-70b-instruct', 'lmsys_score': 1247},
        {'model': 'meta-llama/llama-3.1-405b-instruct', 'lmsys_score': 1267},
        {'model': 'meta-llama/llama-3.1-405b-instruct:bf16', 'lmsys_score': 1266},
        {'model': 'meta-llama/llama-3.2-3b-instruct', 'lmsys_score': 1103},
        {'model': 'meta-llama/llama-3.2-1b-instruct', 'lmsys_score': 1053},
        {'model': 'anthropic/claude-3.5-sonnet', 'lmsys_score': 1283},
        {'model': 'anthropic/claude-3.5-sonnet-20240620', 'lmsys_score': 1268},
        {'model': 'anthropic/claude-3.7-sonnet', 'lmsys_score': 1309},
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
        {'model': 'openai/chatgpt-4o-latest', 'lmsys_score': 1377},  # ChatGPT-4o-latest from image
        {'model': 'google/gemini-2.0-flash-exp', 'lmsys_score': 1355},  # Gemini-2.0-Flash-001
        {'model': 'google/gemini-2.0-flash-thinking-exp-1219', 'lmsys_score': 1384},  # Gemini-2.0-Flash-Thinking-Exp-01-21
        {'model': 'deepseek/deepseek-chat', 'lmsys_score': 1316},  # DeepSeek-V3
        {'model': 'deepseek/deepseek-r1', 'lmsys_score': 1361} # DeepSeek-R1
]

release_dates = [
    {'model': 'openai/gpt-4o-2024-08-06', 'release_date': '2024-08-06'},
    {'model': 'openai/gpt-4o-2024-05-13', 'release_date': '2024-05-13'},
    {'model': 'openai/gpt-4o-mini-2024-07-18', 'release_date': '2024-07-18'},
    {'model': 'openai/gpt-4-0314', 'release_date': '2023-03-14'},
    {'model': 'openai/gpt-4-1106-preview', 'release_date': '2023-11-06'},
    {'model': 'openai/gpt-4-turbo', 'release_date': '2024-04-09'},
    {'model': 'openai/gpt-4.5-preview', 'release_date': '2025-02-27'},
    {'model': 'openai/chatgpt-4o-latest', 'release_date': '2024-08-14'},
    {'model': 'openai/o1-mini', 'release_date': '2024-09-12'},
    {'model': 'openai/o1-preview', 'release_date': '2024-09-12'},
    {'model': 'openai/o1', 'release_date': '2024-12-05'},
    {'model': 'meta-llama/llama-3.1-8b-instruct', 'release_date': '2024-07-23'},
    {'model': 'meta-llama/llama-3.1-70b-instruct', 'release_date': '2024-07-23'},
    {'model': 'meta-llama/llama-3.1-405b-instruct', 'release_date': '2024-07-23'},
    {'model': 'meta-llama/llama-3.1-405b-instruct:bf16', 'release_date': '2024-07-23'},
    {'model': 'meta-llama/llama-3.2-3b-instruct', 'release_date': '2024-09-25'},
    {'model': 'meta-llama/llama-3.2-1b-instruct', 'release_date': '2024-09-25'},
    {'model': 'meta-llama/llama-3.2-90b-vision-instruct', 'release_date': '2024-09-25'},
    {'model': 'meta-llama/llama-3.2-11b-vision-instruct', 'release_date': '2024-09-25'},
    {'model': 'meta-llama/llama-3.3-70b-instruct', 'release_date': '2024-12-06'},
    {'model': 'anthropic/claude-3-5-haiku-20241022', 'release_date': '2024-10-22'},
    {'model': 'anthropic/claude-3.7-sonnet:thinking', 'release_date': '2025-02-24'},
    {'model': 'anthropic/claude-3.7-sonnet', 'release_date': '2025-02-24'},
    {'model': 'anthropic/claude-3.5-sonnet', 'release_date': '2024-10-22'},
    {'model': 'anthropic/claude-3.5-sonnet-20240620', 'release_date': '2024-06-20'},
    {'model': 'anthropic/claude-3-sonnet', 'release_date': '2024-03-04'},
    {'model': 'anthropic/claude-3-opus', 'release_date': '2024-03-04'},
    {'model': 'anthropic/claude-3-haiku', 'release_date': '2024-03-04'},
    {'model': 'google/gemini-flash-1.5-8b', 'release_date': '2024-10-03'},
    {'model': 'google/gemini-flash-1.5-pro', 'release_date': '2024-09-24'},
    {'model': 'google/gemini-2.0-flash-exp', 'release_date': '2024-12-11'},
    {'model': 'google/gemini-2.0-flash-thinking-exp-1219', 'release_date': '2024-12-19'},
    {'model': 'google/gemini-2.0-flash', 'release_date': '2025-02-01'},
    {'model': 'google/gemini-2.0-flash-lite', 'release_date': '2025-02-01'},
    {'model': 'google/gemini-2.0-pro-experimental', 'release_date': '2025-02-01'},
    {'model': 'google/gemini-pro-1.5', 'release_date': '2024-09-24'},
    {'model': 'google/gemma-2-27b-it', 'release_date': '2024-06-27'},
    {'model': 'google/gemma-2-9b-it', 'release_date': '2024-06-27'},
    {'model': 'x-ai/grok-beta', 'release_date': '2024-08-14'},
    {'model': 'mistralai/mixtral-8x22b-instruct', 'release_date': '2024-04-17'},
    {'model': 'mistralai/mistral-large-latest', 'release_date': '2024-11-18'},
    {'model': 'mistralai/mistral-7b-instruct-v0.3', 'release_date': '2024-05-23'},
    {'model': 'deepseek/deepseek-chat', 'release_date': '2025-01-10'},
    {'model': 'openai/o3-mini:high', 'release_date': '2025-01-31'},
    {'model': 'openai/o3-mini:medium', 'release_date': '2025-01-31'},
    {'model': 'openai/o3-mini:low', 'release_date': '2025-01-31'},
    {'model': 'openai/o3', 'release_date': '2025-04-16'},
    {'model': 'openai/o3-pro', 'release_date': '2025-06-10'},
    {'model': 'openai/o4-mini', 'release_date': '2025-04-16'},
    {'model': 'openai/gpt-4.1-nano', 'release_date': '2025-04-01'},
    {'model': 'anthropic/claude-opus-4', 'release_date': '2025-05-22'},
    {'model': 'anthropic/claude-sonnet-4', 'release_date': '2025-05-22'},
    {'model': 'anthropic/claude-opus-4:thinking', 'release_date': '2025-05-22'},
    {'model': 'anthropic/claude-sonnet-4:thinking', 'release_date': '2025-05-22'},
    {'model': 'x-ai/grok-3-beta:thinking', 'release_date': '2025-02-17'},
    {'model': 'x-ai/grok-3-mini-beta:thinking', 'release_date': '2025-02-17'},
    {'model': 'google/gemini-2.5-pro', 'release_date': '2025-03-01'},
    {'model': 'google/gemini-2.5-pro:thinking', 'release_date': '2025-03-01'},
    {'model': 'google/gemini-2.5-flash:thinking', 'release_date': '2025-03-01'},
    {'model': 'deepseek/deepseek-r1-0528', 'release_date': '2025-05-29'},
    {'model': 'mistralai/mistral-saba-25.02', 'release_date': '2025-02-17'},
    {'model': 'mistralai/mistral-small-3.1', 'release_date': '2025-03-17'},
    {'model': 'mistralai/mistral-medium-3', 'release_date': '2025-05-07'},
    {'model': 'mistralai/magistral-small', 'release_date': '2025-06-10'},
    {'model': 'mistralai/magistral-medium', 'release_date': '2025-06-10'},
    {'model': 'mistralai/devstral-small', 'release_date': '2025-05-01'}
]

model_scales = [
    {'model': 'meta-llama/llama-3.1-8b-instruct', 'parameters': 8e9},
    {'model': 'meta-llama/llama-3.1-70b-instruct', 'parameters': 7e10},
    {'model': 'meta-llama/llama-3.1-405b-instruct', 'parameters': 4.05e11},
    {'model': 'meta-llama/llama-3.2-3b-instruct', 'parameters': 3e9},
    {'model': 'meta-llama/llama-3.2-1b-instruct', 'parameters': 1e9},
]

model_subset = [
    # New models needing both thinking and non-thinking tests
    "anthropic/claude-opus-4",
    "anthropic/claude-opus-4:thinking",
    "anthropic/claude-sonnet-4", 
    "anthropic/claude-sonnet-4:thinking",
    "x-ai/grok-3-beta",
    "x-ai/grok-3-beta:thinking",
    "x-ai/grok-3-mini-beta",
    "x-ai/grok-3-mini-beta:thinking",
    "google/gemini-2.0-pro",
    "google/gemini-2.5-pro",
    "google/gemini-2.5-pro:thinking",
    "google/gemini-2.5-flash",
    "google/gemini-2.5-flash:thinking",
    
    # New OpenAI models
    "openai/o3-mini:high",
    "openai/o3-mini:medium", 
    "openai/o3-mini:low",
    "openai/o3",
    "openai/o3-pro",
    "openai/o4-mini",
    "openai/gpt-4.1-nano",
    
    # New other models
    "deepseek/deepseek-r1",
    "deepseek/deepseek-r1-0528",
    "mistralai/mistral-saba-25.02",
    "mistralai/mistral-small-3.1",
    "mistralai/mistral-medium-3", 
    "mistralai/magistral-small",
    "mistralai/magistral-medium",
    "mistralai/devstral-small",
]

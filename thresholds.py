import json
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Define company colors
COMPANY_COLORS = {
    'openai': '#74AA9C',      # OpenAI green
    'meta-llama': '#044EAB',  # Meta blue
    'anthropic': '#D4C5B9',   # Anthropic beige
    'google': '#669DF7',      # Google blue
    'x-ai': '#000000',        # X black
    'mistralai': '#F54E42'    # Mistral red
}

def count_answers(data, coherence_threshold=80, dissimilarity_threshold=80):
    """
    For each model and each question, count answers sequentially until an answer
    fails either the coherence or dissimilarity threshold.
    
    Parameters:
      - coherence_threshold: minimum coherence_score required.
      - dissimilarity_threshold: minimum (embedding_dissimilarity_score*100) required.
    
    Returns:
      A dict mapping model names to total valid answer counts.
    """
    counts = {}
    for model, threshold_groups in data.get('models', {}).items():
        total_count = 0
        for group_key, questions in threshold_groups.items():
            for question, answers in questions.items():
                # Ensure answers are processed in order
                answers_sorted = sorted(answers, key=lambda a: a.get('answer_num', 0))
                for ans in answers_sorted:
                    if (ans.get('coherence_score', 0) < coherence_threshold or 
                        ans.get('embedding_dissimilarity_score', 0) * 100 < dissimilarity_threshold):
                        # Stop counting further answers for this question.
                        break
                    total_count += 1
        counts[model] = total_count
    return counts

# Load JSON data from file (adjust the file name/path as needed)
with open('results/results.json', 'r') as f:
    data = json.load(f)

# Initial threshold values for both metrics.
init_coherence_threshold = 80
init_dissimilarity_threshold = 80

# Calculate initial counts and sort models (highest count at the top)
model_counts = count_answers(data, coherence_threshold=init_coherence_threshold, 
                             dissimilarity_threshold=init_dissimilarity_threshold)
sorted_models = sorted(model_counts.items(), key=lambda x: x[1], reverse=True)
models = [m for m, _ in sorted_models]
counts = [cnt for _, cnt in sorted_models]
colors = [COMPANY_COLORS.get(m.split('/')[0].lower(), '#AAAAAA') for m in models]

# Create the main figure and axis.
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(left=0.25, bottom=0.35)  # reserve space for the sliders

bars = ax.barh(models, counts, color=colors)
ax.set_xlabel("Total Count of Answers")
ax.set_title(f"Total Answers per Model (Ranked) [Coherence ≥ {init_coherence_threshold}, "
             f"Dissimilarity ≥ {init_dissimilarity_threshold}]")
ax.invert_yaxis()  # highest count on top

# Create slider for the coherence threshold
ax_coherence = plt.axes([0.25, 0.2, 0.65, 0.03])
coherence_slider = Slider(ax_coherence, 'Coherence', 0, 100, 
                          valinit=init_coherence_threshold, valstep=1)

# Create slider for the dissimilarity threshold
ax_dissimilarity = plt.axes([0.25, 0.1, 0.65, 0.03])
dissimilarity_slider = Slider(ax_dissimilarity, 'Dissimilarity', 0, 100, 
                              valinit=init_dissimilarity_threshold, valstep=1)

def update(val):
    # Retrieve current slider values.
    coherence_val = coherence_slider.val
    dissimilarity_val = dissimilarity_slider.val
    
    # Recalculate answer counts based on current thresholds.
    model_counts = count_answers(data, coherence_threshold=coherence_val, 
                                 dissimilarity_threshold=dissimilarity_val)
    sorted_models = sorted(model_counts.items(), key=lambda x: x[1], reverse=True)
    models_new = [m for m, cnt in sorted_models]
    counts_new = [cnt for m, cnt in sorted_models]
    colors_new = [COMPANY_COLORS.get(m.split('/')[0].lower(), '#AAAAAA') for m in models_new]
    
    # Update the plot: clear and redraw.
    ax.clear()
    ax.barh(models_new, counts_new, color=colors_new)
    ax.set_xlabel("Total Count of Answers")
    ax.set_title(f"Total Answers per Model (Ranked) [Coherence ≥ {coherence_val}, "
                 f"Dissimilarity ≥ {dissimilarity_val}]")
    ax.invert_yaxis()
    fig.canvas.draw_idle()

# Connect both sliders to the update function.
coherence_slider.on_changed(update)
dissimilarity_slider.on_changed(update)

plt.show()


#!/usr/bin/env python3
"""Seed data for AI Safety Learning Hub."""
import json

MODULES = [
    (1, "Introduction to AI & Transformative AI", "Beginner", "45 min",
     "What is AI, what makes transformative AI different, and why does it matter?", 1),
    (2, "Catastrophic Risk & Failure Modes", "Beginner", "50 min",
     "How advanced AI could cause global catastrophic harm — core failure modes.", 2),
    (3, "LLM Mechanics & Capabilities", "Intermediate", "60 min",
     "How large language models work — transformers, scaling laws, emergent abilities.", 3),
    (4, "Alignment: RLHF & Beyond", "Intermediate", "60 min",
     "Reinforcement Learning from Human Feedback, Constitutional AI, scalable oversight.", 4),
    (5, "Interpretability: Inside the Black Box", "Advanced", "70 min",
     "Mechanistic interpretability — reverse-engineering neural networks.", 5),
    (6, "AI Governance & Policy", "Intermediate", "55 min",
     "Compute governance, model evaluations, export controls, international coordination.", 6),
    (7, "Forecasting & AI Timelines", "Intermediate", "50 min",
     "How experts forecast AI progress — calibration, Fermi estimates, timeline views.", 7),
    (8, "Capstone: Your First AI Safety Project", "Advanced", "90 min",
     "Hands-on project ideas and a step-by-step path to contributing.", 8),
]

LESSONS = {
    1: [("What is AI and ML?", "Artificial Intelligence (AI) is the broad field of building systems that perform tasks normally requiring human intelligence. Machine Learning (ML) is a subset where systems learn patterns from data rather than being explicitly programmed. Deep Learning uses multi-layer neural networks. In recent years, large language models (LLMs) and foundation models have dramatically expanded AI capabilities."),
        ("Transformative AI Defined", "Transformative AI refers to AI that would have a comparable impact on human civilization to the agricultural or industrial revolutions. It is often associated with Artificial General Intelligence (AGI) — systems that can perform most economically valuable work at or above human level."),
        ("Why the Stakes Are Unprecedented", "Advanced AI could amplify human capabilities enormously. This creates both enormous upside (curing disease, accelerating science) and catastrophic downside (accidental loss of control, misuse, rapid concentration of power).")],
    2: [("The Alignment Problem", "The alignment problem is the challenge of getting AI systems to do what humans actually want, rather than what we literally instruct or reward. Even small misalignments compound as systems become more capable."),
        ("Reward Hacking & Specification Gaming", "Reward hacking occurs when an AI finds a way to achieve high reward without doing what designers intended. As systems get smarter, finding loopholes becomes easier."),
        ("Misuse & Proliferation", "Even perfectly aligned AI can be misused by humans — cyberweapons, pathogen design, automated disinformation, arms races. Dual-use technology is a major governance challenge.")],
    3: [("Transformers & Self-Attention", "The Transformer architecture (2017) is the foundation of modern LLMs. Its core mechanism, self-attention, lets the model weigh the importance of every token relative to every other token. This parallelizable design enabled training at unprecedented scale."),
        ("Scaling Laws", "Scaling laws describe predictable relationships between model size (parameters), training data, compute, and performance. Performance improves smoothly following power laws, letting researchers forecast future capabilities."),
        ("Emergent Capabilities & Limits", "As models scale, they gain abilities not explicitly trained for: multi-step reasoning, code generation, tool use. But LLMs also hallucinate confidently and have frozen knowledge.")],
    4: [("RLHF Explained", "Reinforcement Learning from Human Feedback (RLHF): pretrain, collect human rankings, train a reward model, fine-tune via RL (PPO). Makes models helpful, harmless, honest — but inherits human biases and can be jailbroken."),
        ("Constitutional AI & RLAIF", "Constitutional AI scales oversight using AI feedback (RLAIF). The model critiques/revises its own outputs according to a set of principles, reducing reliance on expensive human raters."),
        ("Scalable Oversight & Debate", "As AI surpasses human level, humans cannot directly evaluate outputs. Methods: amplification (AI assistants help humans), debate (AIs argue while humans judge), recursive reward modeling.")],
    5: [("Why Interpretability Matters", "If we cannot understand what a model knows or how it reasons, we cannot reliably detect deception, hidden capabilities, or misalignment. Interpretability opens the black box."),
        ("Mechanistic Interpretability Methods", "Activation patching, feature visualization, circuit analysis, sparse autoencoders for monosemantic features, logit lens. The field is young but progressing rapidly."),
        ("Open Problems", "Scaling to frontier models, understanding superposition, detecting deception and situational awareness, building interpretability-by-design architectures.")],
    6: [("Compute Governance", "Training frontier AI requires enormous compute. This bottleneck can be governed: tracking large clusters, requiring safety evaluations before large training runs, restricting advanced chip access."),
        ("Model Evaluations & Red-Teaming", "Before deployment, run evals testing dangerous capabilities: autonomous replication, cyberoffense, chemical/biological knowledge, persuasion, deception. Red-teaming = experts trying to break the model."),
        ("International Coordination", "AI development is global. Unilateral restrictions risk race dynamics. Effective governance requires international agreements, but geopolitical tensions make coordination hard.")],
    7: [("Why Forecasting Matters", "Policy and strategy depend on timelines. If transformative AI is likely in 5 vs. 50 years, priorities differ dramatically. Forecasting improves resource allocation."),
        ("Calibration & Scoring", "A well-calibrated forecaster: of events assigned 70%, ~70% happen. Brier scores measure accuracy. Techniques: base rates, reference classes, Fermi estimates, Bayesian updating."),
        ("Current Timeline Views", "Expert surveys (AI Impacts, Metaculus, FLI) show wide disagreement. Median estimates for human-level AI range ~2040-2060. Significant minority assigns substantial probability within 10-15 years.")],
    8: [("Project 1: Interpretability Experiment", "Use GPT-2 small (free compute) and try activation patching or logit lens. Can you identify which layers encode factual knowledge vs. reasoning? Document findings in a blog post."),
        ("Project 2: Build an Eval Dataset", "Create a small eval testing a specific failure mode — sycophancy, jailbreak susceptibility, biased outputs. Test against 2-3 open models; publish methodology and results."),
        ("Project 3: Regional Policy Analysis", "Research AI policy in your country/region. What gaps matter for catastrophic risk? Write a policy brief — underrepresented regions produce genuinely novel work."),
        ("Next Steps: Join the Community", "ARENA, SERI MATS, Apollo Research, MAIA, AI Safety Support. Read Alignment Forum, LessWrong, AI Impacts. Attend EAGx. The field is small and welcomes initiative.")],
}

QUIZ = {
    1: [("ML is a subset of AI that:", ["Requires human programmers for every rule", "Learns patterns from data", "Only works on images", "Requires quantum computers"], 1),
        ("Transformative AI would have impact comparable to:", ["A new smartphone", "The industrial revolution", "A software update", "A social media platform"], 1)],
    2: [("The alignment problem is about:", ["Aligning text on a page", "Getting AI to do what humans actually want", "Making AI faster", "Aligning multiple companies"], 1),
        ("Reward hacking is when AI:", ["Rewards humans financially", "Finds a loophole to get high reward without achieving the goal", "Hacks into reward systems", "Refuses rewards"], 1)],
    3: [("The core Transformer mechanism is:", ["Recurrence", "Self-attention", "Convolution", "Decision trees"], 1),
        ("Scaling laws relate performance to:", ["Marketing budget", "Compute, data, and parameters", "Number of employees", "Office size"], 1)],
    4: [("RLHF stands for:", ["Real Learning Human Function", "Reinforcement Learning from Human Feedback", "Recursive Layer Hybrid Fusion", "Reward Learning Human Fine-tuning"], 1),
        ("Scalable oversight is needed because:", ["Humans type too slowly", "Superhuman AI outputs cannot be directly evaluated by humans", "It is cheaper", "It uses less data"], 1)],
    5: [("Mechanistic interpretability aims to:", ["Speed up models", "Reverse-engineer internal computations", "Translate human languages", "Build larger models"], 1),
        ("Activation patching works by:", ["Patching software bugs", "Replacing activations to observe output changes", "Adding layers", "Freezing all weights"], 1)],
    6: [("Compute governance targets:", ["Software licenses", "The GPU/compute bottleneck for training frontier models", "Internet bandwidth", "Electricity prices"], 1),
        ("Red-teaming means:", ["Coloring models red", "Experts deliberately trying to break/jailbreak a model", "Training on red data", "Running on red hardware"], 1)],
    7: [("A well-calibrated forecaster:", ["Is always right", "Of 70% events, ~70% occur", "Never updates", "Only forecasts certain events"], 1),
        ("Fermi estimation involves:", ["Alien calculations", "Breaking problems into parts for order-of-magnitude estimates", "Exact data only", "Asking Fermi"], 1)],
    8: [("Good first interpretability project uses:", ["The largest frontier model", "A small open model like GPT-2 on free compute", "No model at all", "Only proprietary models"], 1),
        ("Which is NOT a recommended next step?", ["Join AI safety communities", "Attend EAGx", "Read Alignment Forum", "Wait for a PhD before doing anything"], 3)],
}

def seed_data(conn):
    for m in MODULES:
        conn.execute("INSERT INTO modules VALUES (?,?,?,?,?,?)", m)
    for mid, lessons in LESSONS.items():
        for title, body in lessons:
            conn.execute("INSERT INTO lessons (module_id, title, body) VALUES (?,?,?)", (mid, title, body))
    for mid, qs in QUIZ.items():
        for q, opts, correct in qs:
            conn.execute("INSERT INTO quiz_questions (module_id, question, options, correct_index) VALUES (?,?,?,?)",
                         (mid, q, json.dumps(opts), correct))

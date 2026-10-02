# Gendered Perceptions of Places in LLMs
## Whose Perspective Does AI Reflect? 
### Auditing Gendered & Geographical Bias in LLMs vs. Real-World Data

## 🎯 Project Objective
The primary objective of this research is to evaluate the reliability and fairness of Large Language Models (LLMs) in providing geographical safety advice, when different gender is making the question. The study seeks to:
* **Quantify Gender Bias:** Measure if LLMs alter safety perceptions based on the gendered persona of the user.
* **Assess Accuracy:** Compare AI safety "intuition" against ground-truth crime statistics and lived human experiences.
* **Evaluate Semantic Alignment:** Determine if AI-generated descriptions of urban spaces reflect the linguistic nuances of actual residents.

## 📖 Overview
As LLMs like GPT-5 and Claude Sonnet 4 become integrated into travel suggestion engines, they risk amplifying historical stereotypes. This case study forensicly audits these models by comparing their outputs for London neighborhoods against 1.6M+ Airbnb reviews and official police data. The research identifies a critical "perception gap" where AI models frequently overestimate risk and introduce gendered disparities that do not exist in the real world.

## 📊 Datasets
The analysis integrates three high-dimensional data pillars:
* **Human Sentiment:** 1.6M+ London Airbnb reviews (2009–2025) providing "lived experience" data.
* **Ground Truth:** 969,175 official crime records from the Metropolitan Police (May 2024 – May 2025).
* **Synthetic AI Data:** 630 systematically engineered prompts from GPT-5 and Claude Sonnet 4, stratified by Male, Female, and Neutral traveler personas.

## 🛠️ Methods
* **Data Engineering:** Mapped all datasets to the granular ONS ward-level for high-resolution geographical analysis.
* **Gender Extraction:** Implemented a hybrid classification approach using **Gender-Guesser** and **Genderize.io**, validated at 98% accuracy.
* **Topic Modeling:** Utilized **BERTopic** to extract latent themes such as Safety, Amenities, and Transportation from unstructured text.
* **Fairness Framework:** Applied **Demographic Parity** and **Equalized Odds** metrics to measure systemic bias across personas.

  **Codes are included, here:** https://drive.google.com/file/d/16iiSC_iAVX1KUeDA_qBjtAuAv77Gx4Vn/view?usp=drive_link

## 🔍 Analysis
The analysis focused on the divergence between AI perception and reality:
* **Similarity Auditing:** Using Sentence Transformers, I calculated the semantic similarity between AI and humans. GPT-5 (0.28) and Claude (0.23) showed weak alignment with actual human descriptions.
* **Correlation Testing:** Employed Spearman’s Rank Correlation to determine if LLM safety ratings actually reflected real-world crime density.
* **Statistical Significance:** Conducted T-tests to validate the safety gaps found between gendered prompts.

## 🏆 Results
* **The Safety Gap:** Human reviews describe 90% of neighborhoods as safe, while LLMs are significantly more cautious (Claude: 52%, GPT-5: 44%).
* **Gendered Protectionism:** LLMs exhibited significant gender bias (Claude: p=0.001, GPT-5: p=0.024), frequently labeling areas as "safe" for women more often than for men—a bias not found in the human dataset.
* **Hallucinated Risk:** GPT-5 specifically misclassified several low-crime areas as high-risk, showing weak alignment with Metropolitan Police data.

## 💡 Impact
This project provides a blueprint for **Responsible AI** in the travel and real estate sectors. It demonstrates that:
* Unfiltered LLM outputs can distort community perceptions and lead to unfair economic disinvestment.
* High-accuracy gender classification and fairness metrics are essential for auditing social-facing AI.
* **Retrieval-Augmented Generation (RAG)** is necessary to ground AI safety advice in real-time facts rather than biased training data.

## 🏁 Conclusion
The study concludes that current state-of-the-art LLMs suffer from "geographical hallucinations" and "gendered sensitivity" that do not reflect ground-truth reality. While human crowdsourced data remains a reliable proxy for urban safety, AI models require significant bias mitigation and data-grounding before being deployed in recommendation engines.

---
**Author:** Kostanca Kovaci  
**Degree:** MSc Data Science, Middlesex University London  
**Advisor:** Dr. Giovanni Quattrone

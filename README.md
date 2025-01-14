<p align="center">
  <img src="https://github.com/mkturkcan/generative-agents/blob/main/assets/logo.png?raw=true"  width="180" />
</p>


# Generative Large Language Models for Human-Like Behavior

This repository includes a working version of the type of model described in Generative Agents: Interactive Simulacra of Human Behavior.

## Setup

The models are distributed as notebooks that are easy to run locally, or on Google Colab. We recommend the use of Jupyter Lab if running locally. The notebook(s) should work as-is on Google Colab.

# How to Use

* The most stable model is available at https://github.com/mkturkcan/generative-agents/tree/main/notebook/Release.
* WIP models with the latest features will be available in https://github.com/mkturkcan/generative-agents/tree/main/notebook/WIP.
* A WIP library is available under https://github.com/mkturkcan/generative-agents/tree/main/game_simulation.

## Model

The current model is a simulation of the town of Phandalin from an introductory D&D 5e adventure. This setting is chosen as it is much more free form than the simple scenario described in the original paper.

## Limitations

The model, as described in the paper, requires access to a very high quality instruction model such as GPT-3. However, the model also requires many high-context queries to work, making it expensive to run. As such, in this work we use low-parameter, locally runnable models instead. 

We expect that with the advent of the next generation of instruction-tuned models, the model in this repo will perform better.

## Future Steps

* Summarize agent decisions as emojis.
* Create a family of questions to compress agent contexts better.
* Check if the agent contexts are compressed well with an another layer of prompts.
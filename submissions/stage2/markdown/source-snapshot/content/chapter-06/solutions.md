# Chapter 6 — Strengths & Limitations

## Explained answers

These are expected answers, not the only acceptable wording. Credit a correct alternative with clear assumptions and reasoning. Try the exercises before reading this section.

### Answer 6.1

An embedded device has limited memory for weights and working data, compute time for deadlines, power from its supply and thermal capacity to remove heat. A model that fits storage can still exceed RAM or latency budgets. Consider quantisation or a smaller model, then measure accuracy and worst-case timing on the target device.

### Answer 6.2

Scalability means accommodating growth while meeting acceptable service targets. Interoperability means exchanging and correctly using information between systems. A network that can carry many packets still fails interoperability if one sensor sends centimetres and the receiver assumes metres. Test load, schemas, units, versions and identities.

### Answer 6.3

Adaptive intelligence changes behaviour appropriately using new evidence or experience. It can respond to changed conditions, but noisy feedback, distribution shifts or unsafe exploration can make adaptation harmful. Test changes against objectives and retain monitoring and recovery controls.

### Answer 6.4

Predictive analytics estimates future or unknown outcomes from evidence, such as a likely equipment failure. Behavioural modelling represents actions and interactions, such as how drivers respond to signs. A model can be useful without proving causes; both require relevant data and evaluation on new cases.

### Answer 6.5

Resource optimisation selects where and how to compute while balancing latency, accuracy, energy, bandwidth, privacy and cost. Local emergency control can avoid a remote round trip; cloud processing can support large-scale training or reporting. Edge processing still has hardware limits and requires maintenance.

### Answer 6.6

Explainability makes relevant aspects of model behaviour understandable to a particular audience. Deep RL can be difficult to explain because many learned parameters and sequential consequences interact. An approximate post-hoc explanation may be useful, but is not a guarantee of the model’s true causal reasoning.

### Answer 6.7

Security concerns include unauthorised commands and replay or manipulation of sensor messages. Ethical concerns include unfair impacts, privacy loss and unclear responsibility for harm. Combine authentication, freshness checks, monitoring, human oversight and explicit accountability. Valid alternative risks and controls should earn credit when well justified.

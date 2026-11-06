# Teaching outline: Networking for behaviorist AI

Open the guide at the pages below. Let learners answer before continuing through a thinking pause. Use the matching Python demonstration to change an input and explain the resulting change.

| Time | Teaching step | Guide page | What to show or ask |
|---|---|---|---|
| 00:00 | Should a robot wait for the cloud? | 75 | Should a robot wait for the cloud? |
| 00:39 | Today’s route | 75 | Today’s route |
| 01:16 | Reactive behaviour is not always learning | 24 | Training may occur centrally while a fixed policy runs locally. |
| 02:04 | Keep the time-critical loop close | 75 | A useful architecture keeps time-critical sensing, policy evaluation and actuator control near the device. |
| 02:55 | Let the network do useful shared work | 89 | Robot: immediate control; Network: telemetry and updates; Server: coordination and analysis |
| 03:44 | A number needs context | 75 | Reject stale or unauthorised commands. |
| 04:33 | Inspect three incoming messages | 75 | Inspect three incoming messages |
| 05:42 | Match feedback to the original action | 75 | Action 42: turn left; Action 43: move forward; Feedback 43 arrives first; Match by recorded identity |
| 06:32 | Define what an outage means | 89 | Continued operation must not be assumed. |
| 07:20 | The feedback packet never arrived | 75 | Missing feedback = reward zero? |
| 08:12 | Connect the responsibilities | 75 | Local control + shared services; Context and authentication; Feedback belongs to its action; Explicit outage behaviour |
| 09:07 | Blue Impulse study guide | 1 | Blue Impulse study guide |

The written tutorial PDF contains the full explanation and exact book excerpts. Numerical examples are teaching models, with assumptions stated in the guide, narration, and supporting file.

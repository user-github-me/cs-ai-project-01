# Teaching outline: Basic reinforcement learning

Open the guide at the pages below. Let learners answer before continuing through a thinking pause. Use the matching Python demonstration to change an input and explain the resulting change.

| Time | Teaching step | Guide page | What to show or ask |
|---|---|---|---|
| 00:00 | How does a rover learn a route? | 25 | How does a rover learn a route? |
| 00:34 | Today’s route | 25 | Today’s route |
| 01:11 | Follow the learning loop | 25 | The objective is usually expected cumulative reward, not just the next reward. |
| 01:52 | Reward, policy, value | 26 | Reward: score now; Policy: choose an action; Value: estimate return |
| 02:34 | The restaurant analogy | 27 | Early estimates can be wrong, so always exploiting can lock an agent into an inferior policy. |
| 03:24 | Is the familiar route certainly best? | 27 | Two successes versus an untried route: proof? |
| 04:05 | What is a Q value? | 28 | Alpha controls the size of an update. Gamma discounts future rewards. |
| 04:49 | Work through the book’s update | 28 | Work through the book’s update |
| 05:45 | A better estimate, not a proof | 28 | It did not prove the action is always best. |
| 06:34 | Try a terminal state | 28 | Terminal state: old Q = 2, α = 0.5, reward = 1 |
| 07:17 | Experience changes estimates | 31 | Observe → act → feedback; Explore and exploit; Q update: 2 → 3.3; Deployment is not necessarily learning |
| 08:07 | Blue Impulse study guide | 1 | Blue Impulse study guide |

The written tutorial PDF contains the full explanation and exact book excerpts. Numerical examples are teaching models, with assumptions stated in the guide, narration, and supporting file.

---
title: 'Policy Gradients: The Straightforward Route to Reinforcement Learning'
date: 2026-01-18 14:20:00
updated: 2026-01-18 14:20:00
description: 'A practical derivation of REINFORCE, reward-to-go, baselines, advantage estimates, and importance sampling.'
categories:
  - article
tags:
  - reinforcement learning
  - policy gradient
  - reinforce
  - importance sampling
  - machine learning
math: true
---

Value based methods learn how good an action is and recover a policy from those values. Policy gradient methods take the more direct route: represent the policy itself with a neural network and adjust its parameters so that high-return actions become more likely.

This direct objective is attractive, especially for continuous actions, but it introduces a difficult estimation problem. A policy changes the distribution of entire trajectories, and the reward of one trajectory can be noisy. The policy gradient derivation explains both why the method works and why practical algorithms need variance reduction.

<!-- more -->

## Optimizing a trajectory distribution

Let a trajectory be

$$
\tau = (s_1,a_1,s_2,a_2,\ldots,s_T,a_T).
$$

If the initial state distribution is $p(s_1)$, the environment transition model is $p(s_{t+1}\mid s_t,a_t)$, and the policy is $\pi_\theta(a_t\mid s_t)$, then the probability of a trajectory is

$$
p_\theta(\tau) = p(s_1)\prod_{t=1}^{T}\pi_\theta(a_t\mid s_t)p(s_{t+1}\mid s_t,a_t).
$$

Only the policy depends on $\theta$. The environment dynamics are part of the distribution, but they are not parameters we can differentiate through in the usual model-free setting.

Define the return of a trajectory as

$$
R(\tau) = \sum_{t=1}^{T}r(s_t,a_t).
$$

The objective is the expected return under the current policy:

$$
J(\theta) = \mathbb{E}_{\tau\sim p_\theta(\tau)}[R(\tau)].
$$

The goal is to maximize $J(\theta)$ with gradient ascent.

## The log-derivative trick

The trajectory space can be enormous or continuous, so we write the expectation as an integral and differentiate it:

$$
\begin{aligned}
\nabla_\theta J(\theta)
&= \int \nabla_\theta p_\theta(\tau)R(\tau)\,d\tau \\
&= \int p_\theta(\tau)\nabla_\theta\log p_\theta(\tau)R(\tau)\,d\tau \\
&= \mathbb{E}_{\tau\sim p_\theta(\tau)}\left[\nabla_\theta\log p_\theta(\tau)R(\tau)\right].
\end{aligned}
$$

The second line uses $\nabla p = p\nabla\log p$. This identity is useful because it lets us estimate the gradient with samples from the policy without differentiating through the unknown transition dynamics.

Now expand the log probability of a trajectory:

$$
\begin{aligned}
\nabla_\theta\log p_\theta(\tau)
&= \nabla_\theta\left(\log p(s_1) + \sum_{t=1}^{T}\log\pi_\theta(a_t\mid s_t) + \log p(s_{t+1}\mid s_t,a_t)\right) \\
&= \sum_{t=1}^{T}\nabla_\theta\log\pi_\theta(a_t\mid s_t).
\end{aligned}
$$

The terms involving the initial state and the environment cancel because they do not depend on $\theta$. Therefore,

$$
\nabla_\theta J(\theta) = \mathbb{E}_{\tau\sim p_\theta(\tau)}\left[\left(\sum_{t=1}^{T}\nabla_\theta\log\pi_\theta(a_t\mid s_t)\right)R(\tau)\right].
$$

This is the policy gradient estimator behind REINFORCE.

## REINFORCE with Monte Carlo samples

With $N$ sampled trajectories, an unbiased estimator is

$$
\widehat{\nabla_\theta J}
= \frac{1}{N}\sum_{i=1}^{N}\left(\sum_{t=1}^{T}\nabla_\theta\log\pi_\theta(a_{i,t}\mid s_{i,t})\right)R(\tau_i).
$$

The update is gradient ascent:

$$
\theta \leftarrow \theta + \alpha\widehat{\nabla_\theta J}.
$$

The algorithm is simple:

1. Roll out the current policy and collect complete trajectories.
2. Compute each trajectory return.
3. Estimate the policy gradient from the sampled actions and returns.
4. Update the policy parameters.

The catch is variance. A single trajectory return is used to reinforce every action in that trajectory, even though early actions may have little connection to rewards received much later. Long horizons make this noise worse, so an unbiased estimator can still be too unreliable to train successfully.

## Causality and reward-to-go

An action at time $t$ cannot affect rewards that were received before time $t$. We can therefore replace the full return with the reward-to-go:

$$
G_t = \sum_{t'=t}^{T}r(s_{t'},a_{t'}).
$$

The estimator becomes

$$
\widehat{\nabla_\theta J}
= \frac{1}{N}\sum_{i=1}^{N}\sum_{t=1}^{T}
\nabla_\theta\log\pi_\theta(a_{i,t}\mid s_{i,t})G_{i,t}.
$$

This causality trick keeps the expectation correct while removing reward terms that cannot be caused by the current action. It usually reduces variance without requiring a value model.

## Baselines and the advantage function

We can subtract a baseline that depends on the state without changing the expected gradient:

$$
\mathbb{E}_{a\sim\pi_\theta(\cdot\mid s)}\left[\nabla_\theta\log\pi_\theta(a\mid s)b(s)\right] = 0.
$$

The best practical baseline is often the state value $V^\pi(s)$. Subtracting it gives the advantage function:

$$
A^\pi(s,a) = Q^\pi(s,a) - V^\pi(s).
$$

The gradient then increases the probability of actions that perform better than the average action at the same state and decreases the probability of worse actions. A learned value network can estimate $V^\pi(s)$, which is the first step from REINFORCE toward actor-critic methods.

## Off-policy learning and importance sampling

REINFORCE is on-policy. After updating $\theta$, old trajectories came from a different policy and are no longer direct samples from $p_\theta(\tau)$. Discarding them is expensive, especially when successive policies are similar.

If samples come from an older policy $\pi_{\theta_{old}}$, importance sampling rewrites the expectation as

$$
\mathbb{E}_{\tau\sim p_\theta}[f(\tau)]
= \mathbb{E}_{\tau\sim p_{\theta_{old}}}\left[\frac{p_\theta(\tau)}{p_{\theta_{old}}(\tau)}f(\tau)\right].
$$

The trajectory ratio is

$$
\frac{p_\theta(\tau)}{p_{\theta_{old}}(\tau)}
= \prod_{t=1}^{T}\frac{\pi_\theta(a_t\mid s_t)}{\pi_{\theta_{old}}(a_t\mid s_t)}.
$$

This product is the main problem. Even if each ratio is close to one, multiplying many ratios can produce extremely small or large weights. The estimator variance can grow rapidly with the horizon, making naive off-policy policy gradients unstable.

Trust region methods address this issue by restricting how far the new policy can move from the behavior policy. Another practical approximation uses state action marginals or clipped ratios instead of a full trajectory ratio. These ideas lead toward methods such as TRPO and PPO, where controlling policy change is as important as following the gradient.

## The main picture

Policy gradients optimize the policy directly through the distribution of trajectories. The log-derivative trick removes the need to know the environment dynamics, and REINFORCE turns the resulting expectation into a Monte Carlo update. Reward-to-go and baselines make the estimator less noisy, while a learned value function leads naturally to actor-critic algorithms.

The method is conceptually direct, not automatically low variance. Long trajectories, sparse rewards, and large policy changes can all make the gradient estimate unreliable. Good policy optimization is therefore a balance between a correct gradient objective and enough variance control to make that objective usable.

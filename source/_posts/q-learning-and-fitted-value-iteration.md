---
title: 'Q-Learning and Fitted Value Iteration'
date: 2025-11-29 14:20:00
updated: 2025-11-29 14:20:00
categories:
  - article
tags:
  - reinforcement learning
  - q-learning
  - value iteration
  - fitted q iteration
  - machine learning
math: true
---

Value functions turn a long-horizon decision problem into a repeated prediction problem. The central question is simple: after reaching a state, how much future reward should we expect? The Bellman operator gives a principled answer, and value iteration repeatedly applies that operator until the estimate becomes consistent with its own one-step lookahead.

The tabular version is elegant, but it breaks down when the state is an image, a robot configuration, or any other high-dimensional continuous object. Fitted value iteration and fitted Q iteration keep the same Bellman idea while replacing the table with a function approximator.

## The Bellman optimality operator

For a value function $V$, the Bellman optimality operator is

$$
(BV)(s) = \max_a \left[r(s,a) + \gamma \mathbb{E}_{s' \sim P(\cdot \mid s,a)}[V(s')]\right].
$$

Here $r(s,a)$ is the immediate reward, $\gamma$ is the discount factor, and $P(\cdot \mid s,a)$ describes the distribution of the next state after taking action $a$ in state $s$. The second term asks how valuable the next state will be after the immediate reward has been collected.

The optimal value function is a fixed point of this operator:

$$
V^* = BV^*.
$$

Finding the fixed point is therefore equivalent to finding the optimal value function. In the tabular setting, this is more than a useful interpretation. When $0 \leq \gamma < 1$, $B$ is a contraction under the infinity norm:

$$
\lVert BV - BW \rVert_\infty \leq \gamma \lVert V - W \rVert_\infty.
$$

Repeated application of $B$ consequently moves estimates toward $V^*$.

## Why a table is not enough

A table works when the state space is small and discrete. It stores one number for every state, or one number for every state action pair in the case of a Q function. That representation becomes impractical as soon as the state is continuous or contains pixels. Two nearly identical images would also be treated as unrelated rows unless we build in some notion of similarity ourselves.

This is the curse of dimensionality. The number of possible states grows too quickly for a table to cover them, and visiting every state is impossible in many real environments. A neural network can share information across related states, but it also changes the convergence story.

## Fitted value iteration

Fitted value iteration keeps the Bellman backup and adds a regression step. Instead of storing a table, we represent the value function with parameters $\phi$:

$$
V_\phi(s) \approx V(s).
$$

At iteration $k$, we use the current estimator to create Bellman targets for a batch of sampled transitions. A value based version has targets of the form

$$
y_i = r_i + \gamma \mathbb{E}_{s' \sim P(\cdot \mid s_i,a_i)}[V_{\phi_k}(s')].
$$

We then fit a new estimator to those targets:

$$
\phi_{k+1} = \arg\min_\phi \frac{1}{N}\sum_{i=1}^{N}\left(V_\phi(s_i) - y_i\right)^2.
$$

This can be written more compactly as

$$
V_{k+1} = \Pi B V_k,
$$

where $B$ is the Bellman operator and $\Pi$ projects the Bellman result back into the family of functions that our model can represent.

The projection is the important difference from the tabular algorithm. The Bellman operator is a contraction under the infinity norm, and a least-squares projection has useful behavior under an appropriate Euclidean norm. Their composition $\Pi B$, however, is not generally a contraction in either of those same guarantees. Fitted value iteration can therefore fail to converge, especially when the function class is nonlinear, the data distribution is limited, or the targets are repeatedly bootstrapped from the same model.

## Fitted Q iteration

In practice it is often convenient to approximate the action value function directly:

$$
Q_\phi(s,a) \approx Q(s,a).
$$

Given transitions $(s_i,a_i,r_i,s'_i)$, the fitted Q target is

$$
y_i = r_i + \gamma \max_{a'} Q_{\phi_k}(s'_i,a').
$$

The next regression step minimizes

$$
\phi_{k+1} = \arg\min_\phi \frac{1}{N}\sum_{i=1}^{N}\left(Q_\phi(s_i,a_i) - y_i\right)^2.
$$

The model is first used to produce targets, then a new set of parameters is fitted on the observed state action pairs. This separation makes the algorithm look like ordinary supervised learning, but the labels are not fixed. They come from the current Q estimate, so every regression step changes the targets that will be used later.

## Is Q-learning just gradient descent?

The tabular Q-learning update is

$$
Q_{t+1}(s_t,a_t) = Q_t(s_t,a_t) + \alpha_t\left[r_t + \gamma \max_{a'}Q_t(s_{t+1},a') - Q_t(s_t,a_t)\right].
$$

The bracketed term is the temporal difference error. The update resembles a gradient step because it moves the current estimate toward a target, but it is more precise to call it a stochastic approximation method. The target itself depends on the current Q function and on a random transition.

With a neural network, we can minimize a squared Bellman error with gradient descent. That optimization step is useful, but it does not turn the whole algorithm into ordinary supervised learning. The labels depend on a changing and sometimes unstable model, and the max operation can amplify estimation errors. Target networks, replay buffers, careful data coverage, and conservative optimization are practical ways to reduce those problems, not proofs that convergence is guaranteed.

## Why Q-learning is off-policy

The data can be collected by a behavior policy that explores the environment, while the target uses the greedy action selected by

$$
\arg\max_{a'} Q_\phi(s',a').
$$

The behavior policy does not need to be the latest greedy policy. This is the meaning of off-policy learning: the policy producing the samples and the policy being evaluated or improved can differ. It is useful because old replay data can remain valuable while the estimated policy changes.

Off-policy does not mean that any data is sufficient. The replay set still needs enough coverage of useful states and actions. If the behavior policy never visits a region of the environment, the Q estimator has no reliable evidence there, no matter how many regression steps are applied.

## The practical picture

The core loop is short:

1. Collect transitions from an exploratory behavior policy.
2. Use the current value or Q estimator to build Bellman targets.
3. Fit the estimator to those targets.
4. Repeat while monitoring both prediction quality and environment returns.

Tabular value iteration has a clean contraction argument. Once a neural approximator and a projection step are introduced, that argument no longer transfers automatically. The right mental model is therefore not that fitted value iteration is guaranteed gradient descent, but that it is repeated Bellman backup followed by approximate regression. It can work very well, but its stability depends on the function class, the data distribution, and the details of the training loop.

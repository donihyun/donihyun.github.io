---
title: Solutions to $e^{e^z}=1$ on the Complex Plane
date: 2026-04-01 11:55:00
categories:
  - article
tags:
  - complex analysis
  - exponential
  - equations
math: true
---

In this note, we solve

$$
e^{e^z}=1, \quad z\in\mathbb{C}.
$$

Let

$$
z=x+iy,\quad x,y\in\mathbb{R}.
$$

## 1) First, solve $e^w=1$

For a complex number $w$, the solutions of $e^w=1$ are

$$
w=2\pi i k,\quad k\in\mathbb{Z}.
$$

Applying this with $w=e^z$, we get

$$
e^z=2\pi i k,\quad k\in\mathbb{Z}.
$$

Since $e^z\neq 0$, we must have $k\neq 0$.

So we need to solve

$$
e^z=2\pi i k,\quad k\in\mathbb{Z}\setminus\{0\}.
$$

## 2) Write $e^z$ in real/imaginary parts

Using

$$
e^z=e^{x+iy}=e^x(\cos y+i\sin y),
$$

and matching real/imaginary parts with $2\pi i k$ gives

$$
e^x\cos y=0,\qquad e^x\sin y=2\pi k.
$$

From $e^x>0$, the first equation implies

$$
\cos y=0 \Rightarrow y=\frac\pi2+n\pi,\ n\in\mathbb{Z}.
$$

Then $\sin y=\pm1$.

- If $k>0$, we need $\sin y=1$, so
  $$
  y=\frac\pi2+2\pi m,\quad m\in\mathbb{Z},
  $$
  and
  $$
  e^x=2\pi k\Rightarrow x=\ln(2\pi k).
  $$

- If $k<0$, we need $\sin y=-1$, so
  $$
  y=\frac{3\pi}2+2\pi m,\quad m\in\mathbb{Z},
  $$
  and
  $$
  e^x=-2\pi k=2\pi|k|\Rightarrow x=\ln(-2\pi k).
  $$

## Final solution set

Therefore,

$$
\boxed{
\begin{aligned}
z&=\ln(2\pi k)+i\left(\frac\pi2+2\pi m\right), &&k\in\mathbb{Z}_{>0},\ m\in\mathbb{Z},\\
z&=\ln(-2\pi k)+i\left(\frac{3\pi}2+2\pi m\right), &&k\in\mathbb{Z}_{<0},\ m\in\mathbb{Z}.
\end{aligned}}
$$

An equivalent compact form is

$$
z=\ln(2\pi|k|)+i\big(\arg(ik)+2\pi m\big),\quad k\in\mathbb{Z}\setminus\{0\},\ m\in\mathbb{Z},
$$

where $\arg(ik)=\frac\pi2$ for $k>0$ and $\arg(ik)=\frac{3\pi}2$ for $k<0$ (mod $2\pi$).

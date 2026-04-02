---
title: Solving exp(exp(z)) = 1 on the Complex Plane
date: 2026-04-01 11:55:00
categories:
  - article
tags:
  - complex analysis
  - exponential
  - equations
math: true
---

## Introduction

In this note, we solve the equation

$$
e^{e^z}=1,
$$

for all complex numbers \(z\in\mathbb{C}\).

A useful idea is to first solve a simpler outer equation, and then pull it back through the inner exponential.

## Step 1: Solve \(e^w=1\)

For complex \(w\),

$$
e^w=1 \quad \Longleftrightarrow \quad w=2\pi i k,\ \ k\in\mathbb{Z}.
$$

Now let \(w=e^z\). Then

$$
e^z=2\pi i k,\qquad k\in\mathbb{Z}.
$$

Since \(e^z\neq 0\), the case \(k=0\) is impossible. So we only consider \(k\in\mathbb{Z}\setminus\{0\}\).

## Step 2: Solve \(e^z=2\pi i k\)

Write \(z=x+iy\) with \(x,y\in\mathbb{R}\). Then

$$
e^z=e^{x+iy}=e^x(\cos y+i\sin y).
$$

Matching real and imaginary parts with \(2\pi i k\):

$$
e^x\cos y=0,
\qquad
 e^x\sin y=2\pi k.
$$

Because \(e^x>0\), the first equation gives \(\cos y=0\), so

$$
y=\frac\pi2+n\pi,\qquad n\in\mathbb{Z}.
$$

Hence \(\sin y=\pm1\), and we split by the sign of \(k\):

- If \(k>0\), then \(\sin y=1\), so
  $$
  y=\frac\pi2+2\pi m,\quad m\in\mathbb{Z},
  $$
  and
  $$
  x=\ln(2\pi k).
  $$

- If \(k<0\), then \(\sin y=-1\), so
  $$
  y=\frac{3\pi}{2}+2\pi m,\quad m\in\mathbb{Z},
  $$
  and
  $$
  x=\ln(-2\pi k).
  $$

## Final Solution Set

Therefore,

$$
\begin{cases}
z=\ln(2\pi k)+i\left(\dfrac\pi2+2\pi m\right), & k>0,\ \ k,m\in\mathbb{Z},\\[6pt]
z=\ln(-2\pi k)+i\left(\dfrac{3\pi}{2}+2\pi m\right), & k<0,\ \ k,m\in\mathbb{Z}.
\end{cases}
$$

Equivalently, with \(k\in\mathbb{Z}\setminus\{0\}\):

$$
z=\ln(2\pi|k|)+i\big(\arg(ik)+2\pi m\big),\qquad m\in\mathbb{Z},
$$

where \(\arg(ik)=\frac\pi2\) when \(k>0\), and \(\arg(ik)=\frac{3\pi}{2}\) when \(k<0\) (mod \(2\pi\)).

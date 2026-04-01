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

We want all complex numbers \(z\in\mathbb{C}\) satisfying

$$
e^{e^z}=1.
$$

Write

$$
z=x+iy,\quad x,y\in\mathbb{R}.
$$

## Step 1: Reduce to an equation of the form \(e^z = \cdots\)

If \(e^w=1\), then

$$
w=2\pi i k,\quad k\in\mathbb{Z}.
$$

Set \(w=e^z\). Then

$$
e^z=2\pi i k,\quad k\in\mathbb{Z}.
$$

Since \(e^z\neq 0\), we must have \(k\neq 0\).

So we solve

$$
e^z=2\pi i k,\quad k\in\mathbb{Z}\setminus\{0\}.
$$

## Step 2: Split into real and imaginary parts

Using

$$
e^z=e^{x+iy}=e^x(\cos y+i\sin y),
$$

we get

$$
e^x\cos y=0,\qquad e^x\sin y=2\pi k.
$$

Because \(e^x>0\), the first equation gives \(\cos y=0\), hence

$$
y=\frac\pi2+n\pi,\quad n\in\mathbb{Z}.
$$

So \(\sin y=\pm1\).

- **Case \(k>0\):** need \(\sin y=1\), so
  $$
  y=\frac\pi2+2\pi m,\quad m\in\mathbb{Z},
  $$
  and
  $$
  x=\ln(2\pi k).
  $$

- **Case \(k<0\):** need \(\sin y=-1\), so
  $$
  y=\frac{3\pi}{2}+2\pi m,\quad m\in\mathbb{Z},
  $$
  and
  $$
  x=\ln(-2\pi k).
  $$

## Final Solution Set

Therefore the complete set of solutions is

$$
z=\ln(2\pi k)+i\left(\frac\pi2+2\pi m\right),\quad k>0,\ k,m\in\mathbb{Z},
$$

or

$$
z=\ln(-2\pi k)+i\left(\frac{3\pi}{2}+2\pi m\right),\quad k<0,\ k,m\in\mathbb{Z}.
$$

Equivalent compact form:

$$
z=\ln(2\pi|k|)+i\big(\arg(ik)+2\pi m\big),\quad k\in\mathbb{Z}\setminus\{0\},\ m\in\mathbb{Z}.
$$

with \(\arg(ik)=\frac\pi2\) for \(k>0\), and \(\arg(ik)=\frac{3\pi}{2}\) for \(k<0\) (mod \(2\pi\)).

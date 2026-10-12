# Differentiation & integration

A small calculus toolkit for probability: differentiation measures how fast a quantity changes; integration adds up its contributions. These two ideas explain the connection between a cumulative distribution function (CDF) and a probability density (PDF).

## Differentiation: how fast is it changing?

Suppose $g(x)=x^2$. Moving from $x$ to $x+h$ changes the output by $(x+h)^2-x^2$. Divide by the input change $h$ to find the **average change per unit**:

$$
\frac{g(x+h)-g(x)}{h}
=\frac{2xh+h^2}{h}=2x+h\qquad(h\ne0).
$$

As $h$ approaches zero, this approaches $2x$. That limiting rate is the **derivative**:

$$
g'(x)=\frac{dg}{dx}=\lim_{h\to0}\frac{g(x+h)-g(x)}h=2x.
$$

The first two notations mean the same thing: differentiate $g$ with respect to $x$. On a graph, this is the slope of the tangent at $x$.

At $x=0.5$, the slope is $1$. A small input increase of $0.01$ therefore gives an output increase of **approximately** $1(0.01)=0.01$. The actual increase is $0.51^2-0.5^2=0.0101$. A derivative describes a local rate; it does not claim that the curve keeps the same slope over a whole interval.

## The differentiation rules you need

Here $c$ is a constant; $u$ and $v$ are differentiable functions of $x$. Apply each rule where the expressions and derivatives exist.

| Expression | Derivative | Example |
|---|---|---|
| $c$ | $0$ | $7\mapsto0$ |
| $x^n$ | $nx^{n-1}$ | $x^3\mapsto3x^2$ |
| $cu$ | $cu'$ | $x^2/12\mapsto2x/12$ |
| $u+v$ or $u-v$ | $u'+v'$ or $u'-v'$ | $x^2+x^3\mapsto2x+3x^2$ |
| $uv$ | $u'v+uv'$ | Differentiate each factor in turn. |
| $g(u(x))$ | $g'(u(x))u'(x)$ | Differentiate the outside, then multiply by the inside's derivative. |

For example, let $g(x)=(x^2+x^3)/12$. Its derivative is

$$
\frac{d}{dx}\left(\frac{x^2+x^3}{12}\right)
=\frac1{12}(2x+3x^2).
$$

The constant factor stays; differentiate each power separately.

<details id="product-and-chain" markdown="1">
<summary>Product and chain rules: a worked example</summary>

We want to differentiate the **complete expression**

$$
H(x)=x^2\arctan\!\left(\sqrt{x^2-1}\right),\qquad x>1.
$$

Here $\arctan z$ means the angle whose tangent is $z$, measured in radians. We use $x>1$ so the square root is positive and the denominators below are nonzero. Our goal is to find $H'(x)$.

### 1. Split the expression into its two factors

The outermost operation is multiplication:

$$
\underbrace{x^2}_{\text{first factor}}
\;\underbrace{\arctan\!\left(\sqrt{x^2-1}\right)}_{\text{second factor}}.
$$

Name these factors

$$
p(x)=x^2,\qquad q(x)=\arctan\!\left(\sqrt{x^2-1}\right).
$$

Then $H(x)=p(x)q(x)$. Both factors change with $x$, so the **product rule** gives

$$
H'(x)=p'(x)q(x)+p(x)q'(x).
$$

The first term differentiates the first factor and leaves the second as it is. The second term leaves the first factor as it is and differentiates the second. We add these two contributions.

Since $p'(x)=2x$, we already have

$$
H'(x)=2x\arctan\!\left(\sqrt{x^2-1}\right)+x^2q'(x).
$$

**The only remaining task is to find $q'(x)$.**

### 2. Look inside the second factor and apply the chain rule

The second factor is built in three stages:

$$
x\;\longrightarrow\;x^2-1
\;\longrightarrow\;\sqrt{x^2-1}
\;\longrightarrow\;\arctan\!\left(\sqrt{x^2-1}\right).
$$

Each stage changes the input passed to the next. The **chain rule** multiplies the rate of the outside operation by the rate of the expression inside it.

First set $u(x)=\sqrt{x^2-1}$. The derivative of $\sqrt{w}$ with respect to its input $w$ is $1/(2\sqrt{w})$. Here that input is $w=x^2-1$, whose derivative with respect to $x$ is $2x$. Therefore

$$
u'(x)=\frac{1}{2\sqrt{x^2-1}}\,(2x)
=\frac{x}{\sqrt{x^2-1}}.
$$

Now $q(x)=\arctan u(x)$. The derivative of $\arctan u$ with respect to its input $u$ is $1/(1+u^2)$. Multiply by $u'(x)$ to account for how that input changes with $x$:

$$
\begin{aligned}
q'(x)
&=\frac{1}{1+u(x)^2}\,u'(x)\\
&=\frac{1}{1+(\sqrt{x^2-1})^2}\,
  \frac{x}{\sqrt{x^2-1}}\\
&=\frac{1}{x^2}\,\frac{x}{\sqrt{x^2-1}}\\
&=\frac{1}{x\sqrt{x^2-1}}.
\end{aligned}
$$

The denominator simplifies because $1+(\sqrt{x^2-1})^2=1+x^2-1=x^2$.

### 3. Substitute back into the product rule

Return to $H'(x)=2xq(x)+x^2q'(x)$ and insert the two expressions we now know:

$$
\begin{aligned}
H'(x)
&=2x\arctan\!\left(\sqrt{x^2-1}\right)
  +x^2\frac{1}{x\sqrt{x^2-1}}\\
&=\boxed{2x\arctan\!\left(\sqrt{x^2-1}\right)
  +\frac{x}{\sqrt{x^2-1}}},\qquad x>1.
\end{aligned}
$$

The two terms come from the two changing factors. The chain rule was needed inside the second factor because its input passes through several operations.

</details>

## Integration: add up small contributions

For a nonnegative function $g$, imagine splitting $[a,b]$ into narrow strips. Each strip has approximate area **height $g(x)$ times width $\Delta x$**. Add the areas and let the strips become arbitrarily thin. The result is the **definite integral**:

$$
\int_a^b g(x)\,dx.
$$

The bottom and top numbers are the starting and ending points. The $dx$ tells us we are accumulating with respect to $x$. Where a function is negative, its integral counts signed area; probability densities are nonnegative.

## Why differentiating accumulated area gives the function

**Integration accumulates area. Differentiation tells us how fast that area grows. The connection is that the rate of growth equals the curve’s height.**

Let’s see why geometrically.

Suppose we have a continuous curve $f(t)$ above the horizontal axis. Fix a starting point $a$, and define

$$
A(x)=\int_a^x f(t)\,dt.
$$

Here $A(x)$ is the **area accumulated from $a$ up to $x$**.

Now move the right boundary a small distance $h$, from $x$ to $x+h$. The area increases by

$$
A(x+h)-A(x).
$$

Geometrically, this is a narrow strip under the curve. Its width is $h$, and its height is approximately $f(x)$, so

$$
A(x+h)-A(x)\approx f(x)\,h.
$$

Dividing by the distance we moved gives

$$
\frac{A(x+h)-A(x)}{h}\approx f(x).
$$

The left side measures **how much area we gain per unit movement of the boundary**. It is also the strip’s average height.

As the strip gets narrower, its average height approaches the curve’s height at $x$. Therefore,

$$
\boxed{
A'(x)
=\lim_{h\to0}\frac{A(x+h)-A(x)}h
=f(x).
}
$$

That is why differentiating an accumulated integral recovers the original function.

## Calculate an integral by reversing differentiation

An **antiderivative** $G$ of $g$ satisfies $G'=g$. Since the derivative of $x^2$ is $2x$,

$$
\int 2x\,dx=x^2+C.
$$

Without bounds, this is an **indefinite integral**: a family of antiderivatives. The arbitrary constant $C$ appears because $x^2$, $x^2+5$, and $x^2-8$ all have derivative $2x$.

For a continuous integrand, the fundamental theorem of calculus gives the useful calculation rule:

$$
\boxed{\int_a^b g(x)\,dx=[G(x)]_a^b=G(b)-G(a).}
$$

**Substitute the upper bound, substitute the lower bound, then subtract.** The constant cancels. For example,

$$
\int_{0.5}^{0.8}2x\,dx=[x^2]_{0.5}^{0.8}
=0.8^2-0.5^2=0.39.
$$

The basic power rule reverses differentiation:

$$
\int x^n\,dx=\frac{x^{n+1}}{n+1}+C,\qquad n\ne-1,
$$

on intervals where the powers are defined. Increase the exponent by one, then divide by that new exponent. Constant factors stay outside, and sums can be integrated term by term. Thus $\int0.3x\,dx=0.15x^2+C$. Check an antiderivative by differentiating it back.

## Substitution and integration by parts

Yes. **Two of the most useful integration techniques come directly from running the chain rule and product rule backwards.**

| Differentiation rule | Corresponding integration technique |
|---|---|
| Chain rule | **Substitution** |
| Product rule | **Integration by parts** |

Let’s work through one complete example of each.

**1. Substitution: recognize a chain rule in reverse.**

Suppose we want to calculate

$$
\boxed{\int 2x\sqrt{x^2+1}\,dx.}
$$

Look at the structure:

- The expression inside the square root is $x^2+1$.
- Its derivative is $2x$.
- That derivative is already multiplying the square root.

This is exactly the pattern the chain rule produces: **a function of an inside expression, multiplied by the derivative of that inside expression.**

Give the inside expression a simpler name:

$$
u=x^2+1.
$$

Then

$$
\frac{du}{dx}=2x,
\qquad\text{written as}\qquad du=2x\,dx.
$$

We can now replace **the whole piece $2x\,dx$** with $du$, and the square root with $\sqrt u$:

$$
\int 2x\sqrt{x^2+1}\,dx
=\int \sqrt u\,du.
$$

That is an ordinary power-rule integral:

$$
\int u^{1/2}\,du
=\frac23u^{3/2}+C.
$$

Finally, replace $u$ with its original expression:

$$
\boxed{\int 2x\sqrt{x^2+1}\,dx
=\frac23(x^2+1)^{3/2}+C.}
$$

We can check the answer using the chain rule:

$$
\frac{d}{dx}\left[\frac23(x^2+1)^{3/2}\right]
=\frac23\cdot\frac32(x^2+1)^{1/2}\cdot2x
=2x\sqrt{x^2+1}.
$$

**Substitution works here because the extra factor required by the chain rule is present in the integrand.**

---

**2. Integration by parts: rearrange the product rule.**

Now suppose we want to calculate

$$
\boxed{\int xe^x\,dx.}
$$

For this example, use the fact that $e^x$ has derivative $e^x$, so an antiderivative of $e^x$ is also $e^x$.

Differentiate the product $xe^x$:

$$
\frac{d}{dx}(xe^x)
=\underbrace{1\cdot e^x}_{\text{differentiate }x}
+\underbrace{x\cdot e^x}_{\text{differentiate }e^x}.
$$

Our desired integrand, $xe^x$, appears on the right. Rearrange:

$$
xe^x=\frac{d}{dx}(xe^x)-e^x.
$$

Now integrate both sides:

$$
\int xe^x\,dx
=xe^x-\int e^x\,dx.
$$

Therefore,

$$
\boxed{\int xe^x\,dx=xe^x-e^x+C.}
$$

The idea is: **differentiating a product gives the term we want plus an extra term. Subtract the accumulated extra term.**

The general rule comes from the same rearrangement:

$$
(uv)'=u'v+uv'
$$

so

$$
\boxed{\int uv'\,dx=uv-\int u'v\,dx.}
$$

It is useful when the new integral is simpler. Here differentiating the factor $x$ reduced it to $1$.

---

There are other techniques too:

- **Simplify or expand first:** turn an expression into powers you can integrate separately.
- **Partial fractions:** split certain fractions of polynomials into simpler fractions.
- **Trigonometric identities or substitutions:** rewrite expressions involving trigonometric functions or square roots.

Choosing the right technique takes practice. A useful first question is:

> **What differentiation rule could have produced this expression?**

An inside expression accompanied by its derivative suggests substitution. A product with a factor that becomes simpler when differentiated often suggests integration by parts.

## Why probability uses both

For a variable with density $f$, the CDF $F(x)=P(X\le x)$ accumulates probability up to $x$:

$$
\boxed{F(x)=\int_{-\infty}^{x}f(t)\,dt,
\qquad F'(x)=f(x)\text{ wherever }f\text{ is continuous}.}
$$

The letter $t$ moves through the integration interval; $x$ is its cutoff. The lower bound $-\infty$ means include all values to the left; regions where $f=0$ contribute nothing.

For example, let $f(t)=2t$ on $0\le t\le1$ and zero elsewhere. Its total area is $[t^2]_0^1=1$. Then

$$
F(x)=\begin{cases}
0,&x<0,\\
\displaystyle\int_0^x2t\,dt=x^2,&0\le x\le1,\\
1,&x>1.
\end{cases}
$$

Integration builds $F$ from $f$; differentiation recovers $f$ on the smooth parts of $F$. Subtracting two accumulated areas gives

$$
P(0.5<X\le0.8)=F(0.8)-F(0.5)=0.39.
$$

A density height is probability **per unit of $x$**. Multiplying by a tiny width gives approximately the probability in that tiny interval. Integrating adds those contributions across the full interval.

**Two details matter:** use each formula only on its stated range, splitting an integral where the formula changes. And if a CDF has a jump, that jump is a point probability: differentiating its smooth pieces alone misses it.

## Try one of each

Differentiate $(x^2+x^3)/12$. Then calculate $\int_1^2 0.3x\,dx$.

<details markdown="1">
<summary>Reveal the two calculations</summary>

$$
\frac{d}{dx}\left(\frac{x^2+x^3}{12}\right)
=\frac{2x+3x^2}{12}.
$$

$$
\int_1^2 0.3x\,dx=[0.15x^2]_1^2
=0.15(2^2)-0.15(1^2)=0.45.
$$

The derivative is a function describing a local rate. The definite integral is a number describing accumulation over a specified interval.

</details>

## Differentiation and integration cheat sheet

Use the tables to recognize a familiar function, then use the rules below to handle sums, products, or functions inside other functions. You can check any proposed antiderivative by differentiating it.

Here $c$ is a constant, $C$ is an arbitrary constant of integration, and trigonometric angles are in **radians**. The exponential base $b$ satisfies $b>0$ and $b\ne1$. Also, $\sec x=1/\cos x$.

### Common derivatives

| Function $f(x)$ | Derivative $f'(x)$ |
|---|---|
| $c$ | $0$ |
| $x^n$ | $nx^{n-1}$ |
| $e^x$ | $e^x$ |
| $b^x$ | $b^x\ln b$ |
| $\ln\lvert x\rvert$ | $1/x$ |
| $\sin x$ | $\cos x$ |
| $\cos x$ | $-\sin x$ |
| $\tan x$ | $\sec^2 x$ |
| $\arctan x$ | $1/(1+x^2)$ |
| $\arcsin x$ | $1/\sqrt{1-x^2}$ |

### Common integrals

These are **indefinite integrals**: each answer is a family of antiderivatives, which is why it includes $C$.

| Integrand $f(x)$ | Antiderivatives $\int f(x)\,dx$ |
|---|---|
| $c$ | $cx+C$ |
| $x^n$, with $n\ne-1$ | $\dfrac{x^{n+1}}{n+1}+C$ |
| $e^x$ | $e^x+C$ |
| $b^x$ | $\dfrac{b^x}{\ln b}+C$ |
| $1/x$ | $\ln\lvert x\rvert+C$ |
| $\sin x$ | $-\cos x+C$ |
| $\cos x$ | $\sin x+C$ |
| $\sec^2 x$ | $\tan x+C$ |
| $1/(1+x^2)$ | $\arctan x+C$ |
| $1/\sqrt{1-x^2}$ | $\arcsin x+C$ |

**Domains:** use these formulas on intervals where the expressions and derivatives are defined. The logarithm and $1/x$ formulas require $x\ne0$; the tangent and secant formulas require $\cos x\ne0$; the arcsine derivative and its matching integral require $-1<x<1$. For arbitrary real powers, $x>0$ is a safe domain; integer powers, for example, also allow negative $x$ wherever defined.

### Rules for combining functions

Here $u$ and $v$ are functions of $x$, primes denote derivatives, and $\alpha,\beta$ are constants.

| Rule | Formula |
|---|---|
| Differentiate a sum or constant multiple | $(\alpha u+\beta v)'=\alpha u'+\beta v'$ |
| Product rule | $(uv)'=u'v+uv'$ |
| Quotient rule, where $v\ne0$ | $\left(\dfrac uv\right)'=\dfrac{u'v-uv'}{v^2}$ |
| Chain rule | $\dfrac{d}{dx}f(u(x))=f'(u(x))u'(x)$ |
| Integrate a sum or constant multiple | $\int(\alpha u+\beta v)\,dx=\alpha\int u\,dx+\beta\int v\,dx$ |

When combining indefinite integrals, collect all constants into one final $+C$.

**Substitution — reverse the chain rule.** If $F'=f$, then

$$
\int f(u(x))u'(x)\,dx=F(u(x))+C.
$$

Look for an inside expression together with its derivative. Write $u=u(x)$ and $du=u'(x)\,dx$ to make the replacement. For a definite integral, change the endpoints to their corresponding $u$ values too.

**Integration by parts — rearrange the product rule.**

$$
\int u(x)v'(x)\,dx=u(x)v(x)-\int u'(x)v(x)\,dx.
$$

Choose the factors so that differentiating $u$ makes the remaining integral simpler; include $+C$ in the final answer.

**Definite integral — ending value minus starting value.** If $f$ is continuous on $[a,b]$ and $F'=f$, then

$$
\int_a^b f(x)\,dx=F(b)-F(a).
$$

There is no final $+C$: the same constant cancels when the two endpoint values are subtracted.

### Remember the inside factor

For a linear inside expression with nonzero slope, differentiation **multiplies** by its slope; integration **divides** by that slope:

$$
\frac{d}{dx}e^{3x}=3e^{3x},
\qquad
\int e^{3x}\,dx=\frac13e^{3x}+C.
$$

Differentiating the answer verifies why the factor $1/3$ is needed: it cancels the $3$ produced by the chain rule. This division shortcut applies to a **constant, nonzero** inside slope; for a general inside function, use substitution and account for its derivative.

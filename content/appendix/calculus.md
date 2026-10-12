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

**Product rule:** both factors change. For $x^2q(x)$,

$$
\frac{d}{dx}[x^2q(x)]=2xq(x)+x^2q'(x).
$$

The first term accounts for changing $x^2$ while keeping $q$ at its current value; the second accounts for changing $q$ while keeping $x^2$ at its current value. Multiplying the two derivatives would miss these contributions. A minus sign before the product applies to both terms.

**Chain rule:** changes pass through layers. For $u(x)=\sqrt{x^2-1}$ and $x>1$, the inside changes at rate $2x$, while the square-root function changes at rate $1/(2\sqrt{x^2-1})$. Multiply the rates:

$$
u'(x)=\frac1{2\sqrt{x^2-1}}(2x)
=\frac{x}{\sqrt{x^2-1}}.
$$

Now add the outer layer $q(x)=\arctan u(x)$. Here $\arctan u$ means the angle whose tangent is $u$, measured in radians; its derivative with respect to $u$ is $1/(1+u^2)$. Therefore

$$
\begin{aligned}
q'(x)&=\frac1{1+u(x)^2}\,u'(x)\\
&=\frac1{1+(x^2-1)}\frac{x}{\sqrt{x^2-1}}\\
&=\frac1{x\sqrt{x^2-1}}.
\end{aligned}
$$

Putting these pieces into the product rule gives the complete derivative, for $x>1$:

$$
\begin{aligned}
\frac{d}{dx}\left[x^2\arctan\sqrt{x^2-1}\right]
&=2x\arctan\sqrt{x^2-1}+x^2\frac1{x\sqrt{x^2-1}}\\
&=2x\arctan\sqrt{x^2-1}+\frac{x}{\sqrt{x^2-1}}.
\end{aligned}
$$

</details>

## Integration: add up small contributions

For a nonnegative function $g$, imagine splitting $[a,b]$ into narrow strips. Each strip has approximate area **height $g(x)$ times width $\Delta x$**. Add the areas and let the strips become arbitrarily thin. The result is the **definite integral**:

$$
\int_a^b g(x)\,dx.
$$

The bottom and top numbers are the starting and ending points. The $dx$ tells us we are accumulating with respect to $x$. Where a function is negative, its integral counts signed area; probability densities are nonnegative.

### Calculate an integral by reversing differentiation

An **antiderivative** $G$ of $g$ satisfies $G'=g$. Since the derivative of $x^2$ is $2x$,

$$
\int 2x\,dx=x^2+C.
$$

Without bounds, this is an **indefinite integral**: a family of antiderivatives. The arbitrary constant $C$ appears because $x^2$, $x^2+5$, and $x^2-8$ all have derivative $2x$.

Why does this recover area? Moving the endpoint by a small amount $h$ adds approximately $g(x)h$ of area. The accumulated area therefore changes at rate $g(x)$: it is an antiderivative of $g$.

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

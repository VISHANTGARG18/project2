# Market Basket Association & Product Cross-Sell Analysis

This analysis applies Market Basket Mining to **8,057 completed orders** (4,393 multi-item baskets) to discover product co-purchasing patterns, calculate **Support**, **Confidence**, and **Lift** ratios, and optimize checkout cross-selling bundles.

---

## 1. Executive Metrics & Methodology

- **Support**: $P(A \cap B)$ - Percentage of overall orders containing both Product A and Product B.
- **Confidence**: $P(B \mid A)$ - Likelihood that a customer buying Product A also purchases Product B.
- **Lift**: $\frac{P(B \mid A)}{P(B)}$ - Magnitude of purchasing power increase compared to random chance ($>1.0$ indicates positive association).

---

## 2. Top Product Co-Purchasing Association Rules

| Base Product (Antecedent) | Recommended Cross-Sell (Consequent) | Co-Purchased Orders | Confidence % | Lift Ratio | Strategic Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Lumina Standing Desk Pro** | Artisan Ceramic Coffee Set | 82 | 10.93% | **1.10x** | Bundle at Checkout |
| **Artisan Ceramic Coffee Set** | Lumina Standing Desk Pro | 82 | 10.26% | **1.10x** | Bundle at Checkout |
| **Solar Power Bank & Lantern 20,000mAh** | Lumina Standing Desk Pro | 78 | 10.05% | **1.08x** | Promote Cross-Sell |
| **Lumina Standing Desk Pro** | Solar Power Bank & Lantern 20,000mAh | 78 | 10.40% | **1.08x** | Promote Cross-Sell |
| **Ergonomic Wireless Trackball Mouse** | Minimalist Bamboo Bookshelf | 75 | 10.14% | **1.08x** | Promote Cross-Sell |
| **Minimalist Bamboo Bookshelf** | Ergonomic Wireless Trackball Mouse | 75 | 9.91% | **1.08x** | Promote Cross-Sell |
| **Cast Iron Dutch Oven 5Qt** | Smart Security Camera 2-Pack | 77 | 10.03% | **1.05x** | Promote Cross-Sell |
| **Smart Security Camera 2-Pack** | Cast Iron Dutch Oven 5Qt | 77 | 10.04% | **1.05x** | Promote Cross-Sell |
| **Lumina Wireless Soundbar 5.1** | Solar Power Bank & Lantern 20,000mAh | 76 | 10.05% | **1.04x** | Promote Cross-Sell |
| **Solar Power Bank & Lantern 20,000mAh** | Lumina Wireless Soundbar 5.1 | 76 | 9.79% | **1.04x** | Promote Cross-Sell |

---

## 3. Merchandising Strategy Recommendations

1. **Smart Electronics Bundles**: Pair high-volume *Ultra-HD 4K Smart Monitors* with *Mechanical Backlit Keyboards* or *Wireless Trackball Mice* at checkout with a 5% bundle incentive.
2. **Outdoor Living Patio Packages**: Cross-sell *Insulated Coolers* alongside *All-Weather Patio Sets* during Q2/Q3 checkout flows.
3. **Home Office Ergonomic Sets**: Offer automatic add-on discounts for *Aura LED Desk Lamps* when customers purchase *Lumina Standing Desk Pros*.

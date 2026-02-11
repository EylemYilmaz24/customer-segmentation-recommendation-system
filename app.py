import pandas as pd
import streamlit as st

st.set_page_config(page_title="Ürün Öneri Sistemi", layout="centered")

st.title("Ürün Öneri Sistemi")

@st.cache_data
def load_rules(path: str = "rules.csv") -> pd.DataFrame:
    df_rules = pd.read_csv(path)
    # antecedents / consequents sütunları genelde frozenset gibi kaydedilir; string olarak gelir.
    return df_rules

rules = load_rules()

# Güvenli şekilde ürün listesini çıkar (antecedents ve consequents içindeki ürün adlarını yakala)
def extract_items(series: pd.Series) -> set:
    items = set()
    for s in series.dropna().astype(str):
        # Basit parse: frozenset({'A', 'B'}) gibi metinden ürünleri ayıkla
        s = s.replace("frozenset(", "").replace(")", "")
        s = s.replace("{", "").replace("}", "").replace("'", "")
        parts = [p.strip() for p in s.split(",") if p.strip()]
        for p in parts:
            items.add(p)
    return items

product_set = set()
if "antecedents" in rules.columns:
    product_set |= extract_items(rules["antecedents"])
if "consequents" in rules.columns:
    product_set |= extract_items(rules["consequents"])

products = sorted([p for p in product_set if p])

selected = st.selectbox("Bir ürün seçin:", options=products)

top_n = st.slider("Kaç öneri gösterilsin?", min_value=3, max_value=15, value=5)

def filter_rules_for_item(df_rules: pd.DataFrame, item: str) -> pd.DataFrame:
    tmp = df_rules.copy()
    # antecedents içinde item geçenleri al
    tmp["ante_str"] = tmp["antecedents"].astype(str)
    tmp = tmp[tmp["ante_str"].str.contains(item, na=False)]
    # confidence varsa ona göre sırala
    if "confidence" in tmp.columns:
        tmp = tmp.sort_values("confidence", ascending=False)
    return tmp

filtered = filter_rules_for_item(rules, selected)

st.subheader("Önerilen Ürünler")

if filtered.empty:
    st.info("Bu ürün için kural bulunamadı. Başka bir ürün seçmeyi deneyin.")
else:
    # consequents’i parse edip listele
    recs = []
    for s in filtered["consequents"].head(50).astype(str):
        s = s.replace("frozenset(", "").replace(")", "")
        s = s.replace("{", "").replace("}", "").replace("'", "")
        parts = [p.strip() for p in s.split(",") if p.strip()]
        recs.extend(parts)

    # benzersizleştir, seçilen ürünü çıkar, ilk top_n’i al
    uniq = []
    for r in recs:
        if r and r != selected and r not in uniq:
            uniq.append(r)

    for r in uniq[:top_n]:
        st.write(f"- {r}")

with st.expander("Kurallar (ilk 10)"):
    show_cols = [c for c in ["antecedents", "consequents", "support", "confidence", "lift"] if c in filtered.columns]
    st.dataframe(filtered[show_cols].head(10), use_container_width=True)

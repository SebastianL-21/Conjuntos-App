import streamlit as st
from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn3

def safe_color_patch(venn_obj, zone_id, color=None, alpha=None):
    patch = venn_obj.get_patch_by_id(zone_id)
    if patch:
        if color:
            patch.set_color(color)
        if alpha is not None:
            patch.set_alpha(alpha)

def ordenado(valores):
    try:
        return sorted(valores, key=lambda x: float(x))
    except:
        return sorted(valores)

def format_elements_for_display(element_set, ordenado_func, max_elements_to_show=3):
    if not element_set:
        return ""
    sorted_elements = ordenado_func(list(element_set))
    display_list = sorted_elements[:max_elements_to_show]
    if len(sorted_elements) > max_elements_to_show:
        display_list.append("...")
    return "\n".join(str(e) for e in display_list)


st.set_page_config(page_title="Conjuntos Visual", layout="centered")
st.title("🔷 Proyecto Final - Teoría de Conjuntos")
st.write("Proyecto de Josué Sebastián Licardié Higueros(202507012), Geankarlo André Girón Ochoa(202508082), Daniel Humberto Ramirez Morales(202508053)")


num_conjuntos = st.slider("¿Cuántos conjuntos deseas ingresar?", 2, 10)
conjuntos = {}
errores = False

for i in range(num_conjuntos):
    nombre = st.text_input(f"Nombre del conjunto #{i + 1}", value=chr(65 + i))
    elementos = st.text_input(f"Elementos del conjunto {nombre} (máx. 15, separados por comas)", key=f"elem_{i}")

    if elementos:
        lista = list(set(e.strip() for e in elementos.split(",") if e.strip()))
        if len(lista) > 15:
            st.error(f"⚠️ El conjunto {nombre} tiene más de 15 elementos.")
            errores = True
        else:
            conjuntos[nombre] = set(lista)


operacion = st.selectbox("Selecciona la operación:", [
    "Unión (∪)",
    "Intersección (∩)",
    "Diferencia (A - B - C...)",
    "Diferencia simétrica (solo 2 conjuntos)"
])


if st.button("📊 Mostrar resultados") and not errores:
    if len(conjuntos) != num_conjuntos:
        st.warning("⚠️ Aún faltan conjuntos por completar.")
    else:
        st.subheader("📋 Conjuntos ingresados:")
        for nombre, conjunto in conjuntos.items():
            st.write(f"**{nombre}** = {{ {', '.join(ordenado(conjunto))} }}")

        nombres = list(conjuntos.keys())
        sets = list(conjuntos.values())
        resultado = set()
        op_valida = True

        if operacion.startswith("Unión"):
            resultado = sets[0].copy()
            for s in sets[1:]:
                resultado |= s
            op_nombre = " ∪ ".join(nombres)

        elif operacion.startswith("Intersección"):
            resultado = sets[0].copy()
            for s in sets[1:]:
                resultado &= s
            op_nombre = " ∩ ".join(nombres)

        elif operacion.startswith("Diferencia"):
            resultado = sets[0].copy()
            for s in sets[1:]:
                resultado -= s
            op_nombre = " - ".join(nombres)

        elif operacion.startswith("Diferencia simétrica"):
            if len(sets) != 2:
                st.error("⚠️ La diferencia simétrica solo se puede aplicar a 2 conjuntos.")
                op_valida = False
            else:
                resultado = sets[0] ^ sets[1]
                op_nombre = f"{nombres[0]} Δ {nombres[1]}"

        if op_valida:
            st.subheader(f"🧮 Resultado de {op_nombre}:")
            st.write(f"**Resultado =** {{ {', '.join(ordenado(resultado))} }}")

            
            st.subheader("📈 Diagrama de Venn")

            if len(sets) == 2:
                A, B = sets
                fig, ax = plt.subplots()
                v = venn2([A, B], set_labels=nombres, ax=ax)

                only_A = A - B
                only_B = B - A
                inter = A & B

                etiquetas = {
                    '10': only_A,
                    '01': only_B,
                    '11': inter
                }

                for zona, conjunto in etiquetas.items():
                    label = v.get_label_by_id(zona)
                    if label:
                        label.set_text(format_elements_for_display(conjunto, ordenado))

                for zona in etiquetas:
                    safe_color_patch(v, zona, color="lightgrey", alpha=0.3)

                if operacion.startswith("Unión"):
                    for zona in etiquetas:
                        safe_color_patch(v, zona, color="skyblue", alpha=0.7)
                elif operacion.startswith("Intersección"):
                    safe_color_patch(v, '11', color="orange", alpha=0.8)
                elif operacion.startswith("Diferencia"):
                    safe_color_patch(v, '10', color="lightgreen", alpha=0.7)
                elif operacion.startswith("Diferencia simétrica"):
                    safe_color_patch(v, '10', color="lightcoral", alpha=0.7)
                    safe_color_patch(v, '01', color="lightcoral", alpha=0.7)

                st.pyplot(fig)

            elif len(sets) == 3:
                A, B, C = sets
                plt.clf()
                plt.close('all')
                fig, ax = plt.subplots()
                v = venn3([A, B, C], set_labels=nombres, ax=ax)

                zonas = {
                    '100': A - B - C,
                    '010': B - A - C,
                    '001': C - A - B,
                    '110': A & B - C,
                    '101': A & C - B,
                    '011': B & C - A,
                    '111': A & B & C
                }

                for zona_id, conjunto in zonas.items():
                    label = v.get_label_by_id(zona_id)
                    if label:
                        label.set_text(format_elements_for_display(conjunto, ordenado))

                for zona in zonas:
                    safe_color_patch(v, zona, color="lightgrey", alpha=0.3)

                if operacion.startswith("Unión"):
                    for zona in zonas:
                        if zonas[zona] & resultado:
                            safe_color_patch(v, zona, color="skyblue", alpha=0.7)
                elif operacion.startswith("Intersección"):
                    for zona in zonas:
                        if zonas[zona] == resultado:
                            safe_color_patch(v, zona, color="orange", alpha=0.9)
                elif operacion.startswith("Diferencia"):
                    for zona in zonas:
                        if zonas[zona] & resultado:
                            safe_color_patch(v, zona, color="lightgreen", alpha=0.7)
                elif operacion.startswith("Diferencia simétrica"):
                    st.warning("⚠️ La diferencia simétrica solo está disponible para 2 conjuntos.")

                st.pyplot(fig)
else:
 st.info("📄 Resultado calculado (no se puede generar diagrama de Venn para más de 3 conjuntos).")
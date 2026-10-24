import streamlit as st

st.set_page_config(page_title="Control de Ventas", page_icon="💰", layout="centered")

st.title("💰 CONTROL DE VENTAS")
st.caption("Calcula tus ingresos, costos y ganancias.")

# GUARDAR LOS RESULTADOS
if "resultados" not in st.session_state:
    st.session_state.resultados = []

# MENÚ PRINCIPAL
opcion = st.sidebar.radio(
    "📋 MENÚ PRINCIPAL", ["Calcular producto", "Resumen de productos"]
)

if opcion == "Calcular producto":

    st.subheader("🛒 Selecciona un producto")

    producto = st.selectbox(
        "¿Qué producto quieres calcular?", ["PAPITAS", "BOLIS", "GALLETAS"]
    )

    st.subheader(f"🧮 Cálculo de {producto}")

    with st.form("formulario_ventas"):

        precio_compra = st.number_input(
            "Precio de compra por producto ($)", min_value=0.0, value=1000.0, step=100.0
        )

        precio_venta = st.number_input(
            "Precio de venta por producto ($)", min_value=0.0, value=1500.0, step=100.0
        )

        cantidad = st.number_input(
            "Cantidad de productos", min_value=1, value=1, step=1
        )

        calcular = st.form_submit_button(
            "🧮 Calcular ganancias", use_container_width=True
        )

    if calcular:

        if precio_compra <= 0 or precio_venta <= 0:
            st.error("Los precios deben ser mayores que cero.")

        else:
            ganancia = precio_venta - precio_compra
            ganancia_total = ganancia * cantidad
            ingresos_ventas = precio_venta * cantidad
            costo_total = precio_compra * cantidad

            resultado = {
                "producto": producto,
                "ingresos": ingresos_ventas,
                "costos": costo_total,
                "ganancia": ganancia_total,
            }

            st.session_state.resultados.append(resultado)

            st.success("¡Cálculo realizado correctamente!")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("💵 Ingresos por ventas", f"${ingresos_ventas:,.0f}")

                st.metric("📦 Costos totales", f"${costo_total:,.0f}")

            with col2:
                st.metric("📊 Ganancia por producto", f"${ganancia:,.0f}")

                st.metric("💰 Ganancia total", f"${ganancia_total:,.0f}")

            if ganancia_total > 0:
                st.success(f"¡Tienes ganancias de ${ganancia_total:,.0f}!")

            elif ganancia_total < 0:
                st.error(f"Hay pérdidas de ${abs(ganancia_total):,.0f}.")

            else:
                st.info("No hay ganancias ni pérdidas.")

elif opcion == "Resumen de productos":

    st.subheader("📊 RESUMEN DE PRODUCTOS")

    resultados = st.session_state.resultados

    if len(resultados) == 0:
        st.info("Todavía no has calculado ningún producto.")

    else:
        for numero, dato in enumerate(resultados, start=1):

            with st.expander(f"{numero}. {dato['producto']}"):
                st.write(f"**Ingresos:** ${dato['ingresos']:,.0f}")

                st.write(f"**Costos:** ${dato['costos']:,.0f}")

                st.write(f"**Ganancia:** ${dato['ganancia']:,.0f}")

        st.divider()

        ingresos_totales = sum(dato["ingresos"] for dato in resultados)

        costos_totales = sum(dato["costos"] for dato in resultados)

        ganancias_totales = sum(dato["ganancia"] for dato in resultados)

        st.subheader("💰 Totales generales")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Ingresos totales", f"${ingresos_totales:,.0f}")

        with col2:
            st.metric("Costos totales", f"${costos_totales:,.0f}")

        st.metric("Ganancia o pérdida total", f"${ganancias_totales:,.0f}")

        if st.button("🗑️ Borrar todos los resultados"):
            st.session_state.resultados = []
            st.rerun()

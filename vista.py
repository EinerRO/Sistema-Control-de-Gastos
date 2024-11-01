from conexionmongo import conectar_mongodb,  insetar_transaccion
from procedimientos import clasificar_monto_transaccion, extraer_monto_ahorro
from flet import * 
import flet
import datetime

def main(page:Page):

    conexion1, conexion2 = conectar_mongodb()

    fecha_actual = datetime.datetime.now()
    mes_actual = fecha_actual.strftime('%m')
    dia_actual = fecha_actual.strftime('%d')
    anio_actual = fecha_actual.strftime('%Y')
    format_fecha = f'{dia_actual}/{mes_actual}/{anio_actual}'

    page.title = "Control de Gastos"
    page.vertical_alignment = "center"
    page.bgcolor = flet.colors.CYAN_800

    tipo_transaccion =  Dropdown(label="Tipo Transacción", text_size=20, prefix_icon=flet.icons.WALLET, color=flet.colors.LIGHT_BLUE_900,
            options=[
                flet.dropdown.Option("Consignación"),
                flet.dropdown.Option("Retiro"),
                flet.dropdown.Option("Transferencia"),
                flet.dropdown.Option("Pago"),
            ],
        )
    
    concepto = Dropdown(label="Concepto", text_size=20, prefix_icon=flet.icons.LOCAL_MALL, color=flet.colors.LIGHT_BLUE_900,
            options=[
                flet.dropdown.Option("Servicios"),
                flet.dropdown.Option("Créditos"),
                flet.dropdown.Option("Pago a Tercero"),
                flet.dropdown.Option("Bono"),
                flet.dropdown.Option("Viaticos"),
                flet.dropdown.Option("Doméstico"),
                flet.dropdown.Option("Ahorro"),
                flet.dropdown.Option("Traslado"),
                flet.dropdown.Option("Salario"),
                flet.dropdown.Option("Ajuste"),
                flet.dropdown.Option("Reverso"),
                flet.dropdown.Option("Otro"),
            ],
        )
    
    valor = TextField(label="Valor", text_size=20, prefix_icon=flet.icons.ATTACH_MONEY, color=flet.colors.LIGHT_BLUE_900)

    def resgistrar_datos(e):
        insetar_transaccion(tipo_transaccion.value, concepto.value, int(valor.value), format_fecha, conexion1)
        tipo_transaccion.value = ""
        concepto.value = ""
        valor.value = ""
        page.update()


    boton_aceptar = ElevatedButton(
        text='Cargar Transacción', 
        width=400, height=50,
        on_click=resgistrar_datos, 
        icon=flet.icons.ADD_CARD_SHARP,
    )

    #GRAFICA DE BARRAS

    pagos = clasificar_monto_transaccion("pagos")
    transferencias = clasificar_monto_transaccion("transferencias")
    retiros = clasificar_monto_transaccion("retiros")
    compras = clasificar_monto_transaccion("compras")
    consignaciones = clasificar_monto_transaccion("consignaciones")
    usos_cupo = clasificar_monto_transaccion("usocupo")
    uso_rindediario = clasificar_monto_transaccion("gastorindediario")
    saldo = clasificar_monto_transaccion("saldorindediario")
    ahorro = extraer_monto_ahorro()
    porcentaje_pagos = (pagos/consignaciones)*100
    porcentaje_transferencias = (transferencias/consignaciones)*100
    porcentaje_retiros = (retiros/consignaciones)*100
    porcentaje_compras = (compras/consignaciones)*100

    grafica_barras = flet.BarChart(
        bar_groups=[
            flet.BarChartGroup(
                x=0,
                bar_rods=[
                    flet.BarChartRod(
                        from_y=0,
                        to_y=pagos,
                        width=40,
                        color=flet.colors.LIGHT_BLUE_900,
                        tooltip=f"{pagos:,.2f}",
                        border_radius=0,
                    ),
                ],
            ),
            flet.BarChartGroup(
                x=1,
                bar_rods=[
                    flet.BarChartRod(
                        from_y=0,
                        to_y=transferencias,
                        width=40,
                        color=flet.colors.LIGHT_BLUE_900,
                        tooltip=f"{transferencias:,.2f}",
                        border_radius=0,
                    ),
                ],
            ),
            flet.BarChartGroup(
                x=2,
                bar_rods=[
                    flet.BarChartRod(
                        from_y=0,
                        to_y=retiros,
                        width=40,
                        color=flet.colors.LIGHT_BLUE_900,
                        tooltip=f"{retiros:,.2f}",
                        border_radius=0,
                    ),
                ],
            ),
            flet.BarChartGroup(
                x=3,
                bar_rods=[
                    flet.BarChartRod(
                        from_y=0,
                        to_y=compras,
                        width=40,
                        color=flet.colors.LIGHT_BLUE_900,
                        tooltip=f"{compras:,.2f}",
                        border_radius=0,
                    ),
                ],
            ),
        ],
        left_axis=flet.ChartAxis(labels_size=40, title=flet.Text("Totales en pesos"), title_size=40),
        bottom_axis=flet.ChartAxis(
            labels=[
                flet.ChartAxisLabel(
                    value=0, label=flet.Container(flet.Text("Pagos"), padding=10)
                ),
                flet.ChartAxisLabel(
                    value=1, label=flet.Container(flet.Text("Transferencias"), padding=10)
                ),
                flet.ChartAxisLabel(
                    value=2, label=flet.Container(flet.Text("Retiros"), padding=10)
                ),
                flet.ChartAxisLabel(
                    value=3, label=flet.Container(flet.Text("Compras"), padding=10)
                ),
            ], labels_size=40
        ),
        horizontal_grid_lines=flet.ChartGridLines(
            color=flet.colors.GREY_300, width=1, dash_pattern=[3, 3]
        ),
        tooltip_bgcolor=flet.colors.with_opacity(0.5, flet.colors.GREY_300),
        # max_y=1000000,
        interactive=True,
        expand=True,
    )
    
    estadisticas = Column([
        Row([
            flet.Container(
                content=Column([
                    Row([flet.Text("Saldo", size=15, font_family="Tahoma", weight=flet.FontWeight.BOLD, color=flet.colors.LIGHT_BLUE_900)]),
                    Row([flet.Icon(name=icons.WALLET_OUTLINED, color=flet.colors.LIGHT_BLUE_900)]),
                    Row([flet.Text(f"${saldo:,.2f}",size=20, font_family="Tahoma", color="#12A14B")]),
                ], spacing=10),
                margin=10,
                padding=10,
                alignment=flet.alignment.center,
                bgcolor="White",
                width=170,
                height=120,
                border_radius=10,
            ),
            flet.Container(
                content=Column([
                    Row([flet.Text("Consignaciones", size=15, font_family="Tahoma", weight=flet.FontWeight.BOLD, color=flet.colors.LIGHT_BLUE_900)]),
                    Row([flet.Icon(name=icons.CURRENCY_EXCHANGE, color=flet.colors.LIGHT_BLUE_900)]),
                    Row([flet.Text(f"${consignaciones:,.2f}",size=20, font_family="Tahoma", color="#12A14B")]),
                ], spacing=10),
                margin=10,
                padding=10,
                alignment=flet.alignment.center,
                bgcolor="White",
                width=170,
                height=120,
                border_radius=10,
            ),
            flet.Container(
                content=Column([
                    Row([flet.Text("Uso Cupo", size=15, font_family="Tahoma", weight=flet.FontWeight.BOLD, color=flet.colors.LIGHT_BLUE_900)]),
                    Row([flet.Icon(name=icons.CREDIT_CARD, color=flet.colors.LIGHT_BLUE_900)]),
                    Row([flet.Text(f"${usos_cupo:,.2f}",size=20, font_family="Tahoma", color="#12A14B")]),
                ]),
                margin=10,
                padding=10,
                alignment=flet.alignment.center,
                bgcolor="White",
                width=170,
                height=120,
                border_radius=10,
            ),
            flet.Container(
                content=Column([
                    Row([flet.Text("Uso Cuenta", size=15, font_family="Tahoma", weight=flet.FontWeight.BOLD, color=flet.colors.LIGHT_BLUE_900)]),
                    Row([flet.Icon(name=icons.TRENDING_DOWN, color=flet.colors.LIGHT_BLUE_900)]),
                    Row([flet.Text(f"${uso_rindediario:,.2f}",size=20, font_family="Tahoma", color="#12A14B")]),
                ]),
                margin=10,
                padding=10,
                alignment=flet.alignment.center,
                bgcolor="White",
                width=170,
                height=120,
                border_radius=10,
            ),
        ]),
        Row([
            flet.Container(
                content=Column([
                    Row([flet.Text("Ahorro", size=15, font_family="Tahoma", weight=flet.FontWeight.BOLD, color=flet.colors.LIGHT_BLUE_900)]),
                    Row([flet.Icon(name=icons.SAVINGS, color=flet.colors.LIGHT_BLUE_900)]),
                    Row([flet.Text(f"${ahorro:,.2f}",size=20, font_family="Tahoma", color="#12A14B")]),
                ]),
                margin=10,
                padding=10,
                alignment=flet.alignment.center,
                bgcolor="White",
                width=170,
                height=120,
                border_radius=10,
            ),
            flet.Container(
                content=Column([
                    Row([
                        flet.Container(
                          content=Column([ 
                            Row([flet.Text("Pagos", size=15, font_family="Tahoma", color="white"), flet.Icon(name=icons.PAYMENTS, color="white")]),
                            Row([flet.Text(f"{round(porcentaje_pagos, 2)}%",size=18, font_family="Tahoma", color="White")], alignment="center")    
                        ]),
                        margin=10,
                        padding=10,
                        alignment=flet.alignment.center,
                        bgcolor=flet.colors.CYAN_800,
                        width=100,
                        height=90,
                        border_radius=10,
                        ),
                        flet.Container(
                          content=Column([ 
                            Row([flet.Text("Transf", size=15, font_family="Tahoma", color="white"), flet.Icon(name=icons.COMPARE_ARROWS_ROUNDED, color="white")], alignment="center"),
                            Row([flet.Text(f"{round(porcentaje_transferencias, 2)}%",size=18, font_family="Tahoma", color="White")], alignment="center")    
                        ]),
                        margin=10,
                        padding=10,
                        alignment=flet.alignment.center,
                        bgcolor=flet.colors.CYAN_800,
                        width=100,
                        height=90,
                        border_radius=10,
                        ),
                        flet.Container(
                          content=Column([ 
                            Row([flet.Text("Retiros", size=15, font_family="Tahoma", color="white"), flet.Icon(name=icons.CREDIT_CARD, color="white")], alignment="center"),
                            Row([flet.Text(f"{round(porcentaje_retiros, 2)}%",size=18, font_family="Tahoma", color="White")], alignment="center")    
                        ]),
                        margin=10,
                        padding=10,
                        alignment=flet.alignment.center,
                        bgcolor=flet.colors.CYAN_800,
                        width=100,
                        height=90,
                        border_radius=10,
                        ),
                        flet.Container(
                          content=Column([ 
                            Row([flet.Text("Compras", size=15, font_family="Tahoma", color="white"), flet.Icon(name=icons.SHOPPING_CART, color="white")], alignment="center", spacing=2),
                            Row([flet.Text(f"{round(porcentaje_compras, 2)}%",size=18, font_family="Tahoma", color="White")], alignment="center")    
                        ]),
                        margin=10,
                        padding=10,
                        alignment=flet.alignment.center,
                        bgcolor=flet.colors.CYAN_800,
                        width=100,
                        height=90,
                        border_radius=10,
                        )
                    ], alignment="center")
                ]),
                margin=10,
                padding=5,
                alignment=flet.alignment.center,
                bgcolor="White",
                width=568,
                height=120,
                border_radius=10,
            ),
        ])
    ])

    ventana_pricipal = Container(
        content=Container(
            content=Row([
                Column([
                    Container(
                        content=Column([
                            Container(
                                content=Row([flet.Text("Registrar Transacción", size=25, font_family="Tahoma",weight=flet.FontWeight.BOLD, color=flet.colors.LIGHT_BLUE_900)], alignment="center"),
                                padding=20,
                                width=500,
                                height=100,
                                border_radius=20,
                                bgcolor="white",
                            ),
                            tipo_transaccion,
                            concepto, 
                            valor, 
                            boton_aceptar,
                            Container(
                                content=Row([flet.TextButton(text="Buscar Transacción", icon="search", icon_color=flet.colors.LIGHT_BLUE_900)], alignment="center"),
                                padding=20,
                                width=500,
                                height=100,
                                border_radius=20,
                                bgcolor="white",
                            ),
                        ], spacing=30),
                        padding=50,
                        width=500,
                        height=650,
                        border_radius=20,
                        bgcolor="white",
                    ),
                ], spacing=10, alignment='center'),

                Column([
                    Container(
                        content=grafica_barras,
                        padding=50,
                        bgcolor="white",
                        width=810,
                        height=320,
                        border_radius=20,
                    ),
                    Container(
                        content=estadisticas,
                        padding=5,
                        bgcolor=flet.colors.with_opacity(0.4, flet.colors.CYAN_50),
                        width=810,
                        height=320,
                        border_radius=20,
                    )
                ])
            ],alignment='center'),padding=20
        ), 
        border_radius=20,
        bgcolor=flet.colors.CYAN_800
    )
    page.add(ventana_pricipal)
    page.update()
flet.app(target=main)
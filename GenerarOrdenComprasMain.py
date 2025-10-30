import os
from Producto import Producto
from DetalleOrdenCompra import DetalleOrdenCompra
from OrdenCompra import OrdenCompra





def cargar_productos(path):
    productos = {}
    
    try:
        fh = open(path, 'r', encoding='cp1252')
    except Exception:
        
        fh = open(path, 'r', encoding='utf-8', errors='replace')

    with fh:
        for linea in fh:
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(';')
            if len(partes) < 5:
                continue
            try:
                codigo = int(partes[0])
                denominacion = partes[1]
                rubro = partes[2]
                marca = partes[3]
                precio = float(partes[4])
            except Exception:
                continue
            productos[codigo] = Producto(codigo, denominacion, rubro, marca, precio)
    return productos


def mostrar_resumen_ordenes(listaOrdenes):
    if not listaOrdenes:
        print("No hay órdenes cargadas aún.")
        return
    print("Órdenes cargadas:")
    for o in listaOrdenes:
        print(f"Número: {o.numero} | Fecha: {o.fecha} | Total: {o.total}")


def cargar_orden(productosDB):
    orden = OrdenCompra()
    detalles_agregados = 0
    while True:
        try:
            codigo_in = input('Ingrese código de producto (o ENTER para finalizar detalles): ').strip()
            if codigo_in == '':
                if detalles_agregados == 0:
                    print('Debe ingresar al menos 1 detalle para la orden.')
                    continue
                break
            codigo = int(codigo_in)
        except ValueError:
            print('Código inválido. Intente nuevamente.')
            continue
        if codigo not in productosDB:
            print(f'El código {codigo} no existe en la base de productos. Intente nuevamente.')
            continue
        producto = productosDB[codigo]
        try:
            cantidad = int(input('Ingrese cantidad: ').strip())
            if cantidad <= 0:
                print('La cantidad debe ser mayor a 0.')
                continue
        except ValueError:
            print('Cantidad inválida. Intente nuevamente.')
            continue
        detalle = DetalleOrdenCompra(cantidad, producto)
        orden.agregar_detalle(detalle)
        detalles_agregados += 1
        print(f'Detalle agregado: {producto.denominacion} x{cantidad} -> Subtotal {detalle.subtotal}')
    print(f'Orden creada: Número {orden.numero} | Total {orden.total}')
    return orden


def mostrar_orden_por_numero(listaOrdenes, numero):
    for o in listaOrdenes:
        if o.numero == numero:
            
            print(f"Orden de Compra N° {o.numero}")
            print(f"Fecha: {o.fecha}")
            print('------------ Productos Comprados ------------------------')
            print('Código Denominación Rubro Marca Cantidad SubTotal')
            for d in o.listaDetalles:
                p = d.producto
                print(f"{p.codigo} {p.denominacion} {p.rubro} {p.marca} {d.cantidad} {d.subtotal}")
            print(f"TOTAL: {o.total}")
            return o
    print(f"La Orden de Compra con número {numero} no existe")
    return None


def generar_archivo_orden(orden, carpeta=None):
    if carpeta is None:
        carpeta = os.path.dirname(__file__)
    nombre = f"ordenCompra_nro_{orden.numero}.txt"
    path = os.path.join(carpeta, nombre)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(f"Orden de Compra N° {orden.numero}\n")
        fh.write(f"Fecha: {orden.fecha}\n")
        fh.write('------------ Productos Comprados ------------------------\n')
        fh.write('Código;Denominación;Rubro;Marca;Cantidad;SubTotal\n')
        for d in orden.listaDetalles:
            p = d.producto
            fh.write(f"{p.codigo};{p.denominacion};{p.rubro};{p.marca};{d.cantidad};{d.subtotal}\n")
        fh.write(f"TOTAL: {orden.total}\n")
    print(f'Archivo generado en: {path}')


def main():
    carpeta = os.path.dirname(__file__)
    productos_path = os.path.join(carpeta, 'productos_compra.txt')
    if not os.path.isfile(productos_path):
        print(f"No se encontró el archivo 'productos_compra.txt' en {carpeta}. Coloque el archivo en la misma carpeta que este script.")
        return
    print(f"Leyendo productos desde: {productos_path}")
    ProductosDataBase = cargar_productos(productos_path)
    print(f'Productos cargados: {len(ProductosDataBase)}')

    listaOrdenCompras = []

    while True:
        print('\nSeleccione una opción:')
        print('a- Ver Orden de Compras Cargadas')
        print('b- Cargar 1 o más Órdenes de Compra')
        print('c- Generar Archivo Orden de Compra por numero')
        print('d- Salir')
        opt = input('Opción: ').strip().lower()
        if opt == 'a':
            mostrar_resumen_ordenes(listaOrdenCompras)
        elif opt == 'b':
            while True:
                orden = cargar_orden(ProductosDataBase)
                listaOrdenCompras.append(orden)
                # solicitar S o N de forma explícita
                while True:
                    resp = input("¿Desea cargar una nueva Orden de Compra? (S/N): ").strip().lower()
                    if resp in ('s', 'n'):
                        break
                    print("Respuesta inválida. Ingrese 'S' para sí o 'N' para no.")
                if resp == 's':
                    continue
                break
        elif opt == 'c':
            try:
                nro = int(input('Ingrese número de Orden de Compra: ').strip())
            except ValueError:
                print('Número inválido')
                continue
            orden = mostrar_orden_por_numero(listaOrdenCompras, nro)
            if orden:
                # solicitar S o N de forma explícita
                while True:
                    gen = input("¿Desea generar el archivo de la Orden de Compra? (S/N): ").strip().lower()
                    if gen in ('s', 'n'):
                        break
                    print("Respuesta inválida. Ingrese 'S' para sí o 'N' para no.")
                if gen == 's':
                    generar_archivo_orden(orden)
                else:
                    print('No se generó el archivo.')
        elif opt == 'd':
            print('Saliendo...')
            break
        else:
            print('Opción inválida. Intente nuevamente.')


if __name__ == '__main__':
    main()

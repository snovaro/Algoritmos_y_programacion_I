# Crucigrama
Este fue mi primer trabajo practico realizado en FIUBA. El ejercicio consistia en el desarrollo de un crucigrama en un tablero de 20x20 donde entren se tengan que adivinar 12 palabras. Cuenta con unos detalle adicionales que son:
    - Se desconoce la posicion de la palabra, es decir, se tienen las definiciones por un lado y el tablero incompleto por el otro y o se sabe que definicion esta asociada a que ubicacion libre del tablero.
    - Cada vez que se comete un error al intentar adivinar una palabra se lanza un dado:
        >Si el resultado del dado es 1 o 2: SE ELIMINA LA ULTIMA PALABRA ADIVINADO Y SE VUELVE A MEZCLAR EL TABLERO
        >Si el resultado del dado es 3 o 4: SE REVELAN LAS VOCALES EN EL TABLERO
        >Si el resultado del dado es 5: EL USUARIO PUEDE EJEGIR UNA PALABRA PARA REVELAR
        >Si el resultado del dado es 6: TERMINA EL JUEGO
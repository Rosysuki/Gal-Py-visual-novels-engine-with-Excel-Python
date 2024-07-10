RUN: bool = True

while True:

    for event in EVENTS():

        match event.type:

            case QUIT:
                RUN: bool = not RUN

            case KEYDOWN:
                
                match event.key:

                    case DEFAULT:
                        pass

            case MOUSEDOWN:
                x ,y = POS

            case DEFAULT:
                pass


// Codigo para Probar Camara (Toma una foto cada vez que se presiona el boton)

#include <TinyMLShield.h>

bool captureFlag = false; // Estado de boton inicia desactivado
byte image[176 * 144 * 2]; // QCIF: 176x 144 x 2 bytes per pixel (RGB565)
int bytesPerFrame; // Cantidad de bytes por foto
int contador;

void setup() {
  Serial.begin(115200);
  while (!Serial); // Se espera hasta que haya conexion serial

  initializeShield(); // Se inicializa boton

  // Initialize the OV7675 camera
  if (!Camera.begin(QCIF, RGB565, 1, OV7675)) { // Parametros: Resolucion, formato, fps, nombre. Supported FPS: 1, 5, 10, 15, 30
    Serial.println("Failed to initialize camera");
    while (1);
  }
  bytesPerFrame = Camera.width() * Camera.height() * Camera.bytesPerPixel(); // Se calcula la cantidad de bytes por foto
}

void loop() {
  bool clicked = readShieldButton();
  contador = 0;
  //if (clicked && !captureFlag) {
  delay(4000);
  if (true) {
    while(contador <= 50){
      captureFlag = true; // Set the activa cuando el boton es presionado
      Camera.readFrame(image);
      for (int i = 0; i < bytesPerFrame - 1; i += 2) { // Se imprime cada pareja de bytes separados por una coma
        Serial.print("0x");
        Serial.print(image[i+1], HEX);
        Serial.print(image[i], HEX);
        if (i != bytesPerFrame - 2) {
          Serial.print(", ");
        }
      }
      Serial.println();
      //delay(5000); // Delay de 1s para evitar succesions rapidas de captura
      contador += 1;
    }
    captureFlag = true; // Se desactiva despues de la captura
  }
}
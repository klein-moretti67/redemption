#include "raylib.h"

int main(void) {
    InitWindow(400, 200, "Raylib on Mint!");
    while (!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(RAYWHITE);
        DrawText("It's alive!", 150, 90, 20, MAROON);
        EndDrawing();
    }
    CloseWindow();
    return 0;
}

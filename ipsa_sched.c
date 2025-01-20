#include <stdio.h>
#include "FreeRTOS.h"
#include "task.h"

// Périodes des tâches (en ticks)
#define PERIOD_STATUS    (1000 / portTICK_PERIOD_MS)
#define PERIOD_CONVERT   (700  / portTICK_PERIOD_MS)
#define PERIOD_MULTIPLY  (750  / portTICK_PERIOD_MS)
#define PERIOD_BINARY    (600  / portTICK_PERIOD_MS)

// -- Tâche 1 : Affiche un message périodiquement
void vTaskPrintStatus(void *pvParameters)
{
    for (;;)
    {
        printf("[T1] Le système fonctionne normalement\n");
        vTaskDelay(PERIOD_STATUS);
    }
}

// -- Tâche 2 : Convertit une valeur Fahrenheit fixe en Celsius
void vTaskTempConversion(void *pvParameters)
{
    const float fixeFahrenheit = 95.0f;
    for (;;)
    {
        float celsius = (fixeFahrenheit - 32.0f) * 5.0f / 9.0f;
        printf("[T2] %.1f°F => %.1f°C\n", fixeFahrenheit, celsius);
        vTaskDelay(PERIOD_CONVERT);
    }
}

// -- Tâche 3 : Multiplie deux grands nombres
void vTaskBigNumMultiply(void *pvParameters)
{
    unsigned long a = 123456789;
    unsigned long b = 987654321;
    for (;;)
    {
        unsigned long resultat = a * b;
        printf("[T3] Multiplication : %lu\n", resultat);
        vTaskDelay(PERIOD_MULTIPLY);
    }
}

// -- Tâche 4 : Fait une recherche binaire dans un tableau de 50 éléments
void vTaskBinarySearch(void *pvParameters)
{
    int tableau[50];
    for (int i = 0; i < 50; i++) {
        tableau[i] = i + 1;  // Rempli de 1 à 50
    }
    int cible = 25; // Valeur à chercher

    for (;;)
    {
        int left = 0, right = 49, found = -1;
        while (left <= right)
        {
            int mid = (left + right) / 2;
            if (tableau[mid] == cible)
            {
                found = mid;
                break;
            }
            else if (tableau[mid] < cible)
                left = mid + 1;
            else
                right = mid - 1;
        }
        if (found != -1)
            printf("[T4] %d trouvé à l'indice %d\n", cible, found);
        else
            printf("[T4] %d non trouvé\n", cible);

        vTaskDelay(PERIOD_BINARY);
    }
}

// -- Fonction d'initialisation et lancement de l'ordonnanceur
int main(void)
{
    xTaskCreate(vTaskPrintStatus,   "T1_Print",     configMINIMAL_STACK_SIZE, NULL, 2, NULL);
    xTaskCreate(vTaskTempConversion,"T2_Convert",   configMINIMAL_STACK_SIZE, NULL, 2, NULL);
    xTaskCreate(vTaskBigNumMultiply,"T3_Multiply",  configMINIMAL_STACK_SIZE, NULL, 1, NULL);
    xTaskCreate(vTaskBinarySearch,  "T4_BinSearch", configMINIMAL_STACK_SIZE, NULL, 1, NULL);

    vTaskStartScheduler();
    return 0; // On ne devrait jamais revenir ici
}

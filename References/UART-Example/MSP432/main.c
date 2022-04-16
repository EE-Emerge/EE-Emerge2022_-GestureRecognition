// Gesture Recognition
// 02/01/22
// UART Attempt


#include <ti/devices/msp432p4xx/driverlib/driverlib.h>
#include <stdio.h>

void delay_ms(uint8_t ms);

const eUSCI_UART_ConfigV1 uartConfig =
{
    EUSCI_A_UART_CLOCKSOURCE_SMCLK,          // SMCLK Clock Source
    78,                                     // BRDIV = 78
    2,                                       // UCxBRF = 2
    0,                                       // UCxBRS = 0
    EUSCI_A_UART_NO_PARITY,                  // No Parity
    EUSCI_A_UART_LSB_FIRST,                  // MSB First
    EUSCI_A_UART_ONE_STOP_BIT,               // One stop bit
    EUSCI_A_UART_MODE,                       // UART mode
    EUSCI_A_UART_OVERSAMPLING_BAUDRATE_GENERATION  // Oversampling
};


int main(void)
{
    /* Halting WDT  */
    WDT_A_holdTimer();

    // Number to be received from serial communication
    char receivedData;

    // Intialize Pin3.2 and 3.3 for UART
    GPIO_setAsPeripheralModuleFunctionInputPin(GPIO_PORT_P3,
                GPIO_PIN2 | GPIO_PIN3, GPIO_PRIMARY_MODULE_FUNCTION);

    GPIO_setAsOutputPin(GPIO_PORT_P2, GPIO_PIN1);
    GPIO_setOutputLowOnPin(GPIO_PORT_P2, GPIO_PIN1);

    /* Setting DCO (clock) to 12MHz */
    CS_setDCOCenteredFrequency(CS_DCO_FREQUENCY_12);

    /* Configuring UART Module */
    UART_initModule(EUSCI_A2_BASE, &uartConfig);

    /* Enable UART module */
    UART_enableModule(EUSCI_A2_BASE);  // UART 3: A2, UART 2: A1, etc...

    while(1)
    {
        // Receive data
        receivedData = UART_receiveData(EUSCI_A2_BASE);

        if(receivedData == 'h'){
            GPIO_setOutputHighOnPin(GPIO_PORT_P2, GPIO_PIN1);
            delay_ms(250);
            GPIO_setOutputLowOnPin(GPIO_PORT_P2, GPIO_PIN1);
        }

    }
}

void delay_ms(uint8_t ms){
    SysTick->LOAD = (3000000*ms)-1;                    // Example: Delay 2 seconds: 3000000Hz * 2000ms = 6000000 ------> Reload Value = 6000000 - 1 = 5999999
    SysTick->VAL = 0;
    SysTick_enableModule();
    while((SysTick->CTRL & 0x10000) == 0);             // While COUNTFLAG is not 0, keep decrementing STCVR
    SysTick_disableModule();
}

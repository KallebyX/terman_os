export const print = {
  async receipt(html: string): Promise<void> {
    const printWindow = window.open('', '_blank');
    if (!printWindow) {
      throw new Error('Não foi possível abrir a janela de impressão');
    }

    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
        <head>
          <title>Comprovante</title>
          <style>
            body {
              font-family: monospace;
              margin: 0;
              padding: 20px;
            }
            @media print {
              body {
                width: 80mm;
              }
            }
          </style>
        </head>
        <body>
          ${html}
        </body>
      </html>
    `);

    printWindow.document.close();
    printWindow.focus();

    return new Promise((resolve) => {
      printWindow.onafterprint = () => {
        printWindow.close();
        resolve();
      };
      printWindow.print();
    });
  },

  async report(html: string): Promise<void> {
    const printWindow = window.open('', '_blank');
    if (!printWindow) {
      throw new Error('Não foi possível abrir a janela de impressão');
    }

    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
        <head>
          <title>Relatório</title>
          <style>
            body {
              font-family: Arial, sans-serif;
              margin: 0;
              padding: 20px;
            }
            @media print {
              body {
                width: 210mm;
              }
            }
          </style>
        </head>
        <body>
          ${html}
        </body>
      </html>
    `);

    printWindow.document.close();
    printWindow.focus();

    return new Promise((resolve) => {
      printWindow.onafterprint = () => {
        printWindow.close();
        resolve();
      };
      printWindow.print();
    });
  }
}; 
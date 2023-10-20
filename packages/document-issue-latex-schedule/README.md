# Quarto First Steps

## Installation

Download Quarto
```bash
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.3.450/quarto-1.3.450-linux-amd64.deb
```

Install Quarto
```bash
sudo dpkg -i quarto-1.3.450-linux-amd64.deb 
sudo apt-get install -f 
```

Install tinytex
```bash
quarto install tinytex
```

## Generate PDF from MD

To generate the PDF examples from the MD files, run the following command:
```bash
quarto render examples/**/document.md --to pdf
```
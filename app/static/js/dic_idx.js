document.addEventListener("DOMContentLoaded", async (event) => {
    dic_pdf = new DicPDF();

    pdf_container = document.getElementById("pdf-container");
    const pdf_name = pdf_container.dataset.name;
    const page_from = parseInt(pdf_container.dataset.from);
    const page_to = parseInt(pdf_container.dataset.to);

    if (await dic_pdf.check(pdf_name)) {
        await dic_pdf.load(pdf_container, pdf_name, page_from, page_to);
    } else {
        pdf_container.innerHTML = "Lisää omistamasi sanakirja asetuksista nähdäksesi sivun koskien tätä indeksiä.";
    }
});
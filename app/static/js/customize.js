document.addEventListener("DOMContentLoaded", async (event) => {
    dic_pdf = new DicPDF();

    const dics = document.querySelectorAll(".dic");
    dics.forEach(async (dic) => {
        const name = dic.dataset.name;
        const check_input = dic.querySelector('input[type="checkbox"]');
        const file_input = dic.querySelector('input[type="file"]');
        if (await dic_pdf.check(name)) {
            check_input.checked = true;
            file_input.disabled = true;
        } else {
            check_input.disabled = true;
            file_input.disabled = false;
        }
    });

    const form = document.getElementById("customize-form");
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const dics = document.querySelectorAll(".dic");
        for (const dic of dics) {
            const name = dic.dataset.name;
            const check_input = dic.querySelector('input[type="checkbox"]');
            const file_input = dic.querySelector('input[type="file"]');

            const file = file_input.files[0];
            if (file && file.type === "application/pdf") {
                await dic_pdf.save(file, name);
                await dic_pdf.check(name);
                file_input.disabled = true;
            } else if (!check_input.checked) {
                await dic_pdf.delete(name);
            }
        }

        form.submit();
    })
});
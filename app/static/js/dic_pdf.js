pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js';

class DicPDF {
    DB_NAME = "dic_db";
    STORE_NAME = "dic_store";

    get_db = () => {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.DB_NAME, 2);

            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                if (!db.objectStoreNames.contains(this.STORE_NAME))
                    db.createObjectStore(this.STORE_NAME);
            };

            request.onsuccess = (event) => {
                const db = event.target.result;
                resolve(db);
            }

            request.onerror = (event) => {
                reject(event.target.errorCode);
            };
        });
    }
    
    get_store = async (mode = "readwrite") => {
        const db = await this.get_db();
        const transaction = db.transaction([this.STORE_NAME], mode);
        const store = transaction.objectStore(this.STORE_NAME);
        return store;
    }

    save = async (file, name) => {
        const file_reader = new FileReader();

        return new Promise((resolve, reject) => {
            file_reader.onload = async () => {
                const data = new Uint8Array(file_reader.result);
                const store = await this.get_store();
                store.put(data, name);
                resolve();
            }

            file_reader.onerror = () => {
                reject(file_reader.error);
            };

            file_reader.readAsArrayBuffer(file);
        });
    }

    load = async (container, name, page_from, page_to) => {
        const store = await this.get_store("readonly");
        const request = store.get(name);
        request.onsuccess = (event) => {
            const data = event.target.result;
            this.#render(container, data, page_from, page_to);
        };
    }

    check = async (name) => {
        const store = await this.get_store("readonly");

        return new Promise((resolve, reject) => {
            const request = store.get(name);

            request.onsuccess = (event) => {
                const data = event.target.result;
                data ? resolve(true) : resolve(false);
            };

            request.onerror = (event) => reject(false);
        });
    }

    delete = async (name) => {
        const store = await this.get_store("readwrite");
        const request = store.delete(name);

        request.onsuccess = (event) => {
            console.log(`Deleted ${name} successfully`);
        };
    }
    
    #render = async (container, data, page_from, page_to) => {
        const loading_task = pdfjsLib.getDocument({ data });
        const pdf = await loading_task.promise;

        for (let page_num = page_from; page_num <= page_to; page_num++) {
            const page = await pdf.getPage(page_num);

            const canvas = document.createElement("canvas");
            canvas.className = "row";
            const ctx = canvas.getContext("2d");

            const viewport = page.getViewport({ scale: 1.5 });
            canvas.width = viewport.width;
            canvas.height = viewport.height;

            container.appendChild(canvas);

            const renderContext = {
                canvasContext: ctx,
                viewport: viewport
            };

            await page.render(renderContext).promise;
        }
    }
}

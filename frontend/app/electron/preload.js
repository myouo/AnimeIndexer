const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("appConfig", {
  apiBase: "http://localhost:8000",
});

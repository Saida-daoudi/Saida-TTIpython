import { useState, useEffect } from "react";
import Prism from "prismjs";
import "prismjs/themes/prism-tomorrow.css";
import "prismjs/components/prism-python";

export default function SnapStylePage() {
  const [selectedFilter, setSelectedFilter] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  
  const filters = [
  { id: 0, name: "origin", icon: "/icons/cartoon.png" },
  { id: 1, name: "gray", icon: "/icons/cartoon.png" },
  { id: 2, name: "invert", icon: "/icons/cartoon.png" },
  { id: 3, name: "sepia", icon: "/icons/cartoon.png" },
  { id: 4, name: "hsv", icon: "/icons/cartoon.png" },

  { id: 5, name: "red_channel", icon: "/icons/cartoon.png" },
  { id: 6, name: "green_channel", icon: "/icons/cartoon.png" },
  { id: 7, name: "blue_channel", icon: "/icons/cartoon.png" },

  { id: 8, name: "brightness_up", icon: "/icons/cartoon.png" },
  { id: 9, name: "brightness_down", icon: "/icons/cartoon.png" },

  { id: 10, name: "contrast_up", icon: "/icons/cartoon.png" },
  { id: 11, name: "contrast_down", icon: "/icons/cartoon.png" },

  { id: 12, name: "saturation_up", icon: "/icons/cartoon.png" },
  { id: 13, name: "saturation_down", icon: "/icons/cartoon.png" },

  { id: 14, name: "gamma_correction", icon: "/icons/cartoon.png" },

  { id: 15, name: "blur", icon: "/icons/cartoon.png" },
  { id: 16, name: "gaussian_blur", icon: "/icons/blur.png" },
  { id: 17, name: "median_blur", icon: "/icons/canny.png" },
  { id: 18, name: "bilateral_blur", icon: "/icons/sepia.png" },
  { id: 19, name: "motion_blur", icon: "/icons/blur.png" },
  { id: 20, name: "box_blur", icon: "/icons/blur.png" },
  { id: 21, name: "average_blur", icon: "/icons/Sharpen.png" },

  { id: 22, name: "cartoon", icon: "/icons/cartoon.png" },
  { id: 23, name: "pencil", icon: "/icons/cartoon.png" },
  { id: 24, name: "pencil_color", icon: "/icons/cartoon.png" },
  { id: 25, name: "sketch", icon: "/icons/cartoon.png" },
  { id: 26, name: "stylization", icon: "/icons/emboss.png" },
  { id: 27, name: "detail", icon: "/icons/emboss.png" },
  { id: 28, name: "oil_paint", icon: "/icons/emboss.png" },
  { id: 29, name: "water_paint", icon: "/icons/emboss.png" },
  { id: 30, name: "hdr", icon: "/icons/emboss.png" },

  { id: 31, name: "summer_effect", icon: "/icons/emboss.png" },
  { id: 32, name: "winter_effect", icon: "/icons/emboss.png" },
  { id: 33, name: "retro_effect", icon: "/icons/emboss.png" },

  { id: 34, name: "canny", icon: "/icons/canny.png" },
  { id: 35, name: "sobelx", icon: "/icons/emboss.png" },
  { id: 36, name: "sobely", icon: "/icons/emboss.png" },
  { id: 37, name: "laplacian", icon: "/icons/emboss.png" },
  { id: 38, name: "scharr", icon: "/icons/emboss.png" },
  { id: 39, name: "prewitt", icon: "/icons/emboss.png" },
  { id: 40, name: "roberts", icon: "/icons/emboss.png" },

  { id: 41, name: "edge_enhance", icon: "/icons/emboss.png" },

  { id: 42, name: "erode", icon: "/icons/emboss.png" },
  { id: 43, name: "dilate", icon: "/icons/emboss.png" },
  { id: 44, name: "open", icon: "/icons/emboss.png" },
  { id: 45, name: "close", icon: "/icons/emboss.png" },
  { id: 46, name: "morph_gradient", icon: "/icons/emboss.png" },
  { id: 47, name: "tophat", icon: "/icons/emboss.png" },
  { id: 48, name: "blackhat", icon: "/icons/emboss.png" },

  { id: 49, name: "binary", icon: "/icons/emboss.png" },
  { id: 50, name: "binary_inv", icon: "/icons/emboss.png" },
  { id: 51, name: "otsu", icon: "/icons/emboss.png" },
  { id: 52, name: "adaptive_mean", icon: "/icons/emboss.png" },
  { id: 53, name: "adaptive_gaussian", icon: "/icons/emboss.png" },
  { id: 54, name: "threshold_tozero", icon: "/icons/emboss.png" },
  { id: 55, name: "threshold_trunc", icon: "/icons/emboss.png" },

  { id: 56, name: "sharpen", icon: "/icons/sharpen.png" },
  { id: 57, name: "emboss", icon: "/icons/emboss.png" },
  { id: 58, name: "edge", icon: "/icons/sharpen.png" },
  { id: 59, name: "outline", icon: "/icons/sharpen.png" },
  { id: 60, name: "custom_kernel", icon: "/icons/sharpen.png" },

  { id: 61, name: "noise", icon: "/icons/sharpen.png" },
  { id: 62, name: "gaussian_noise", icon: "/icons/sharpen.png" },
  { id: 63, name: "salt_pepper_noise", icon: "/icons/sharpen.png" },
  { id: 64, name: "speckle_noise", icon: "/icons/sharpen.png" }
];

  useEffect(() => {
    Prism.highlightAll();
  }, [code]);

  const handleUpload = (e) => {
    const file = e.target.files[0];
    setImageFile(file);
    setPreview(URL.createObjectURL(file));
    setSelectedFilter(null);
    setCode("");
  };

  const applyFilterHandler = async (filter) => {
  if (!imageFile) return;

  setLoading(true);

  const form = new FormData();
  form.append("image", imageFile);
  form.append("filter", filter.name); // ✅ هنا الحل

  try {
    const res = await fetch("http://127.0.0.1:5000/api/process", {
      method: "POST",
      body: form,
    });

    const data = await res.json();

    setPreview(data.imageUrl);
    setCode(data.pythonCode);
    setSelectedFilter(filter);
  } catch (err) {
    console.error(err);
    alert("Error applying filter");
  } finally {
    setLoading(false);
  }
};

  const copyCode = () => {
    if (!code) return;
    navigator.clipboard.writeText(code);
    alert("Python code copied!");
  };

  const resetImage = () => {
    if (imageFile) setPreview(URL.createObjectURL(imageFile));
    setSelectedFilter(null);
    setCode("");
  };

  const toggleDarkMode = () => setDarkMode(!darkMode);

  return (
    <div
      className="snap-container"
      style={{
        backgroundColor: darkMode ? "#fff" : "#000",
        color: darkMode ? "#000" : "#fff",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Main Row: Image + Code + Right Icons */}
      <div
        className="main-row"
        style={{
          display: "flex",
          flex: 1,
          gap: "12px",
          padding: "16px",
        }}
      >
        {/* Image + Code */}
        <div className="flex" style={{ display: "flex", flex: 1, gap: "12px" }}>
          {/* Image */}
          <div style={{ flex: 1, display: "flex", justifyContent: "center", alignItems: "center" }}>
            {preview ? <img src={preview} alt="Uploaded" style={{ maxHeight: "50vh", objectFit: "contain", borderRadius: "12px" }} /> : <span>Upload an image</span>}
          </div>

          {/* Code */}
          {selectedFilter && code && (
            <div
              className="code-block"
              style={{
                flex: 1,
                backgroundColor: "rgba(0,0,0,0.8)",
                color: "#dcdcdc",
                padding: "12px",
                borderRadius: "8px",
                overflowX: "auto",
                maxHeight: "50vh",
              }}
            >
              <div className="code-header" style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ background: "none" }}>{selectedFilter.name}.py</span>
                <button onClick={copyCode}>📋 </button>
              </div>
              <pre className="line-numbers">
                <code className="language-python">{code}</code>
              </pre>
            </div>
          )}
        </div>

        {/* Right Icons */}
        <div
          className="right-icons"
          style={{
            marginTop: "auto",
            marginBottom: "auto",
            display: "flex",
            flexDirection: "column",
            gap: "12px",
            alignItems: "center",
          }}
        >
          <input type="file" onChange={handleUpload} id="fileUpload" style={{ display: "none" }} />
          <label htmlFor="fileUpload" style={iconStyle}>📁</label>
          <button onClick={resetImage} style={iconStyle}>🔄</button>
          <button onClick={toggleDarkMode} style={iconStyle}>{darkMode ? "🌙" : "☀️"}</button>
        </div>
      </div>

      {/* Filters */}
      <div className="filter-bar" style={{backgroundColor: darkMode ? "#fcfcfcff" : "#000", border: darkMode ? "2px solid" : "none" ,borderRadius: darkMode ? "10px" : "none",color: darkMode ? "#000" : "#000000ff",}}>
        {filters.map((f) => (
          <div
            key={f.id}
            className={`filter-button ${selectedFilter?.id === f.id ? "selected" : ""}`}
            style={{backgroundColor: darkMode ? "#444343ff" : "", color: darkMode ? "#ffffffff" : "#000000ff",}}
            onClick={() => applyFilterHandler(f)}
          >
            <img src={f.icon} alt={f.name} className="filter-icon" />
            <span className="filter-name">{f.name}</span>
          </div>
        ))}
      </div>

      {loading && <span style={{ color: "#ccc", textAlign: "center" }}>Applying filter...</span>}
    </div>
  );
}

const iconStyle = {
  width: "40px",
  height: "40px",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  backgroundColor: "rgba(255,255,255,0.2)",
  borderRadius: "8px",
  fontSize: "20px",
  cursor: "pointer",
  marginTop: "auto",
  marginBottom: "auto",
};
// export async function processImage(file, filter) {
//   const form = new FormData();
//   form.append("image", file);
//   form.append("filter", filter);

//   const res = await fetch("http://127.0.0.1:5000/api/process", {
//     method: "POST",
//     body: form,
//   });

//   const blob = await res.blob();
//   return URL.createObjectURL(blob);
// }














export async function processImage(file, filter) {
  const form = new FormData();
  form.append("image", file);
  form.append("filter", filter);

  const res = await fetch("/api/process", {
  method: "POST",
  body: form
});

  const data = await res.json();
  return {
    imageUrl: `data:image/jpeg;base64,${data.image}`,
    pythonCode: data.code
  };
}

















// // export async function processImage(file, filterName) {
// //   const formData = new FormData();
// //   formData.append("file", file);
// //   formData.append("filter", filterName);

// //   const response = await fetch("/apply_filter", {  // <--- هنا
// //     method: "POST",
// //     body: formData,
// //   });

// //   return response.blob(); 
// // }





















// export async function processImage(file, filterName) {
//   const formData = new FormData();
//   formData.append("file", file);
//   formData.append("filter", filterName);

//   const response = await fetch("http://localhost:5000/apply_filter", {
//     method: "POST",
//     body: formData,
//   });

//   if (!response.ok) {
//     throw new Error("Network response was not ok");
//   }

//   const blob = await response.blob();
//   return URL.createObjectURL(blob);
// }


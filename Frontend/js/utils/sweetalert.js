import Swal from "https://cdn.jsdelivr.net/npm/sweetalert2@11.26.25/+esm";
export async function showSweetalert(text, icon) {
  return await Swal.fire({
    text: text,
    icon: icon,
  });
}

export async function showSweetalertConfirmed(text, icon) {
  let result = await Swal.fire({
    text: text,
    icon: icon,
    allowOutsideClick: false,
  });
  return result.isConfirmed;

}

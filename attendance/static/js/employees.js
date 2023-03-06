function deleteClick() {
  const de = document.getElementById('po');
  console.log(('通った？'));
  const c = confirm('削除してよろしいですか？');
  if(c==true){
    de.type = "submit";
  }

}

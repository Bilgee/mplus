Wiki_Model_training file-г jupyter notebook ашиглан нээнэ.
    1) wikipedia api ашиглан сургах датаг цуглуулна.
    2) Цуглуулсан датаг ашиглан Newtopic, Tdictionary, болон Sdictionary file-уудыг гаргаж авна.
Шинээр үүсгэсэн file-уудыг одоо байгаа (mplus/language дотор) тухайн хэлний file-д хамгийн доор нь хуулна.
Sdictionary file-д шинээр нэмж буй үгийн ойролцоо утгатай үгсийг нэмнэ.( "television_camera": ["camera", 0.7368421052631579] )

Анхаарах зүйлс:
Sdictionary-д үг давхцуулалгүй нэмэх ( нэмэх үг байгаа эсэхийг шалгах )
Шинээр нэмэх үг Tdictionary-д байгаа тохиолдолд тухайн үгний list-д нэмэх, байхгүй бол хамгийн доор шинээр нэмж өгөх
Topic-н index нь newtopic file-н list-н байрлалаар дугаарласан дугаар (0 index ni Newtopic file доторхи хамгийн эхний topic). Тийм учраас шинээр нэмэх topic-г file-н төгсгөлд нэмнэ.


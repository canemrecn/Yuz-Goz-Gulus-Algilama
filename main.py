import cv2
#Gerekli kütüphaneleri import et
yuzCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('Cascades/haarcascade_eye.xml')
smileCascade = cv2.CascadeClassifier('Cascades/haarcascade_smile.xml')
# Yüz, göz ve gülümseme sınıflandırıcıları tanımlanıyor
kamera = cv2.VideoCapture(0)
# Kamera açılıyor
kamera.set(3,1280) # genişlik
kamera.set(4,720) # yükseklik
# Kamera ayarları yapılıyor (genişlik ve yükseklik)
dosyaad = None # 'goz_saptama.mp4'
kaydedici = None
# Video kaydetme için gerekli değişkenler tanımlanıyor
while True:
    ret, kare = kamera.read()
# Kameradan kare okunuyor
    gri = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)
# Kare griye dönüştürülüyor
    yuzler = yuzCascade.detectMultiScale(
        gri,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (20, 20)
    )
# Yüz tanıma yapılıyor
    for (x,y,w,h) in yuzler:
        cv2.ellipse(kare,(int(x+w/2),int(y+h/2)),(w//2,h//2),5,0,360,(255,0,0),2)
        gri_kutu = gri[y:y+h, x:x+w]
        renkli_kutu = kare[y:y+h, x:x+w]
        gozler = eyeCascade.detectMultiScale(
            gri_kutu,
            scaleFactor=1.05,
            minNeighbors=5,
            minSize=(40,40)
        )
        for (ex, ey, ew, eh) in gozler:
            cv2.ellipse(renkli_kutu, (int(ex+ew/2),int(ey+eh/2)),
                        (int(ew/2), int(eh/2)),5,0,360,(0, 255, 0), 2)
        gulusler = smileCascade.detectMultiScale(
            gri_kutu,
            scaleFactor=1.5,
            minNeighbors=20,
            minSize=(60,60)
        )
        for (sx, sy, sw, sh) in gulusler:
            cv2.rectangle(renkli_kutu, (sx, sy), (sx + sw, sy + sh), (0, 0, 255),2)
# Yüzler çerçeveleniyor ve gözler, gülümsemeler tespit ediliyor
    cv2.imshow('kare',kare)
# Kare gösteriliyor
    if kaydedici is None and dosyaad is not None:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # .mp4
        kaydedici = cv2.VideoWriter(dosyaad, fourcc, 24.0, (kare.shape[1], kare.shappe[0]), True)
    if kaydedici is not None:
        kaydedici.write(kare)
    k = cv2.waitKey(10) & 0xff
    if k == 27 or k == ord('q'):
        break
kamera.release()
if kaydedici:
    kaydedici.release()
cv2.destroyAllWindows()
#if kaydedici is None and dosyaad is not None:: Eğer kaydedici değişkeni henüz tanımlanmamışsa ve
# dosyaad değişkeni boş değilse, video kaydedici oluşturulur.
#fourcc = cv2.VideoWriter_fourcc(*'mp4v'): Video codec'i belirtilir (MP4 formatı).
#kaydedici = cv2.VideoWriter(dosyaad, fourcc, 24.0, (kare.shape[1], kare.shape[0]), True): Video
# kaydedici oluşturulur ve kayıt başlatılır.
#if kaydedici is not None:: Eğer video kaydedici başarıyla oluşturulmuşsa, kaydediciye kareler
# eklenir.
#k = cv2.waitKey(10) & 0xff: Klavyeden bir tuşun basılıp basılmadığı kontrol edilir.
#if k == 27 or k == ord('q'): break: Eğer ESC tuşuna veya 'q' tuşuna basılmışsa döngüden
# çıkılır.
#kamera.release(): Kamera kaynağı serbest bırakılır.
#if kaydedici: kaydedici.release(): Eğer video kaydedici tanımlıysa, kaydedici serbest
# bırakılır.
#cv2.destroyAllWindows(): Pencereler kapatılır.
# TRUBA HPC - SLURM BETİK OLUŞTURUCU

[![en](https://img.shields.io/badge/ReadMe-English-blue?style=for-the-badge&link=https%3A%2F%2Fgithub.com%2Faugalip%2Ftruba-hpc-slurm-generator%2Fblob%2Fmain%2FREADME.tr.md)](https://github.com/augalip/truba-hpc-slurm-generator/blob/main/README.md)

Yüksek Performanslı Hesaplama (HPC) alanında, verimlilik çok önemlidir. Ancak, özellikle kendi gereksinimleri olan birden çok küme ile karşı karşıya olunduğunda, Slurm betiklerini manuel olarak oluşturmak zaman alıcı ve hata yapmaya açıktır.

Bunu ele almak için, Slurm betiklerinin otomatik oluşturulmasını sağlayan bir Python betiği geliştirdim, böylece iş akışınız daha verimli hale gelir ve hata riski azalır.

Ancak, debug kuyrukları mevcutken neden bu betiği kullanmalısınız? Debug kuyrukları faydalı olabilir, ancak bu araç, betiklerinizin debug kuyruklarına gönderilmeden önce gözden geçirilmesini sağlar ve hata ihtimalini azaltır.

Bu araçla, mevcut kod tabanınıza kolayca entegre edebilir ve ihtiyaçlarınıza uyacak şekilde özelleştirebilirsiniz. Peki, bu araç tam olarak neler yapıyor?

- Betiğin başlık kısmını otomatik olarak doldurur. (Çalışma sayısı ne olursa olsun, onlarca/yüzlerce e-posta almak istemeyebileceğiniz için posta kısmını boş bırakabilirsiniz)
- Talep edilen Truba kümesinin mevcut olup olmadığını kontrol eder. Örneğin, betiğiniz "short" veya "mid1" kümesini talep ediyorsa, bunlar Truba belgelerine uygun olarak otomatik olarak "hamsi"ye dönüştürülür (Bkz: https://docs.truba.gov.tr/TRUBA/kullanici-el-kitabi/hesaplamakumeleri.html)
- Talep edilen iş süresinin Truba tarafından tanımlanan maksimum değerlerle uyumlu olup olmadığını kontrol eder. Ayrıca, geçersiz süreleri (ör. 0-00:15:75) geçerli olanlara dönüştürür (ör. 0-00:16:15).
- Talep edilen düğüm sayısının, Truba'nın fiziksel kapasitesinden küçük olup olmadığını kontrol eder ve herhangi bir hatayı düzeltir.
- Talep edilen çekirdek sayısının, talep edilen düğüm sayısı ve seçilen kümeyle uyumlu olup olmadığını kontrol eder ve herhangi bir hatayı düzeltir.

(Muhtemelen oldukça uzun bir zaman içinde) Yapılacaklar:
- CUDA kümeleri için GPU vs minimum çekirdek sayısı koşullarını kontrol etme.
- Farklı kümeler için mevcut düğüm sayısını kontrol edebilme ve başlangıçta talep edilen çekirdek sayısı ve ram miktarını göz önünde bulundurarak alternatif kümeler önerme yeteneği.





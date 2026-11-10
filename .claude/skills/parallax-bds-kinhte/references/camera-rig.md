# Camera rig: phối cảnh, API, công thức move, nối take

## 1. Mô hình

```
#w-stage   perspective: P (mặc định 1000px) — ống kính
 └ #w-cam  transform-style: preserve-3d — cả thế giới; CHỈ script đặt transform
    ├ .w-layer[data-depth=3000]  trời
    ├ .w-layer[data-depth=1800]  skyline xa
    ├ ...
    ├ .w-layer[data-depth=0]     mặt phẳng tiêu cự (biểu đồ, bản đồ, nhãn chính)
    └ .w-layer[data-depth=-350]  tiền cảnh (cột, cây, mây) — đi nhanh nhất
HUD (ngoài #w-stage)            chữ khoá màn hình, không đi theo camera
```

- Lớp ở độ sâu `d` được đặt `translateZ(-d) scale((P+d)/P)`: lúc camera ở gốc, mọi thứ hiện đúng kích thước đã thiết kế, nên có thể bố trí từng lớp như bố trí trên khung 1920×1080.
- Camera pan `x` (đo trên mặt phẳng tiêu cự) làm điểm ở độ sâu `d` trôi `x·P/(P+d)` px. Hệ số parallax của lớp = `P/(P+d)`: d = −350 → 1,54 (nhanh hơn camera); 0 → 1; 900 → 0,53; 3000 → 0,25.
- Dolly `z` (> 0 là tiến vào) phóng lớp theo `P/(P+d−z)`: lớp gần phóng nhanh hơn lớp xa → parallax theo chiều sâu khi push-in. Lớp có `P+d−z` < 0,3P mờ dần, < 0,12P biến mất (bay xuyên qua thay vì chọc vào ống kính).
- `orbit`/`tilt` xoay thế giới quanh điểm đang nhìn. Lớp là các tấm phẳng, nên giữ |orbit| ≤ 6–8°, quá mức sẽ thấy mép tấm (hiệu ứng "sách pop-up").

## 2. API của rig

Hai template dùng chung rig. `template/compositions/dive.html` (dọc, bay vào bản đồ) điều khiển dolly bằng **zoom**:

```js
const at = (t, lx, ly, zoom, tilt = 0, orbit = 0) => ...; // nhắm điểm (lx,ly) của bản đồ (depth 0)
const KEYS = [
  at(0, 560, 980, 0.85),          // mở rộng, đã đang chạy
  at(3.5, 300, 700, 1.8, 6, -2),  // xuyên mây, lặn xuống
  at(10.5, 690, 1280, 2.5, 10, 3) // tới dự án, bản đồ nghiêng 10°
];
```

- `zoom` = độ phóng của mặt bản đồ, nội suy theo `log(zoom)` (lặn đều như flycam), quy ra dolly `z = P·(1 − 1/zoom)`.
- `tilt` (rotateX) nghiêng bản đồ như flycam nhìn xiên, ≤ 12°: ghim/thẻ ở depth âm "đứng" trên mặt đất và trượt so với bản đồ → parallax ngay cả trên bản đồ phẳng. `orbit` (rotateZ) xoay quanh điểm nhìn, ≤ 6°.
- Giới hạn: lớp depth `d` phải giữ `P + d − z ≥ 0,3P` → với nhãn −30, thẻ −60 thì zoom ≤ ~2,8. Lặn sâu hơn (châu lục → phố) dùng video `bake-basemap` làm lớp bản đồ, hoặc ghép nhiều ảnh bản đồ chi tiết tăng dần (ảnh chi tiết đặt chồng đúng vị trí, hiện dần khi zoom tới).

`template-ngang/compositions/world.html` dùng `z` trực tiếp:

```js
const P = 1000;           // khớp với CSS perspective
const DUR = 20;           // khớp data-duration của host
const FLOAT = 3;          // rung "flycam" tất định (px), 0 = tắt
const look = (d, lx, ly) => ...;  // đặt điểm (lx,ly) của lớp depth d vào giữa khung
const KEYS = [
  { t: 0,  x: -300, y: -120, z: -150, orbit: -4, tilt: 2 },
  { t: 8,  ...look(300, 3000, 430), z: 380, orbit: 3 },
  { t: 20, x: 5240, y: 40, z: -250, orbit: -3, tilt: 1 },
];
```

- Mỗi kênh (x, y, z, orbit, tilt) nội suy **Hermite đơn điệu** (Fritsch–Carlson): đi qua đúng các key, vận tốc liên tục, không vọt lố. Một kênh đổi chiều tại key thì vận tốc kênh đó về 0 ở đó — sắp key sao cho lúc ấy kênh khác vẫn chạy.
- Key đầu: camera *đã đang chạy* khi video mở (độ dốc = đoạn đầu). Key cuối: đáp nhẹ về 0. `stop: true` ở một key = cố ý dừng mọi kênh tại đó.
- Thời gian camera chạy bằng một tween duy nhất `clock.t: 0 → DUR` (ease `none`) trên timeline; mọi thứ là hàm của thời gian nên render tất định, seek ngược xuôi đều đúng.
- Nhãn/biểu đồ nằm trong lớp thì animate bằng GSAP như thường (đã đặt sẵn `fromTo`). Không animate `transform` của `.w-layer` hay `#w-cam` bằng GSAP — rig sở hữu chúng.

## 3. Tốc độ mặc định (khi không có video mẫu)

| Thông số | Giá trị |
| --- | --- |
| Pan trên mặt phẳng tiêu cự | 8–25 %W/s (150–480 px/s ở 1920) — đo trên màn hình, lớp xa chậm hơn |
| Dolly vào vật thể | z +200…+450 trong 3–5 s |
| Kéo lùi kết | z −200…−300 trong 2,5–4 s |
| Orbit | 0,5–1,5 °/s, tổng ≤ 8° |
| Khoảng cách giữa key | 2,5–4 s; key trùng với cụm lời dẫn |
| Khoảng cách tới vật thể khi tới nơi | vật thể chiếm 35–60% chiều cao khung |

Kiểm tra bằng `analyze_refs.py` trên bản render: pan/zoom trung vị nằm trong khoảng p50–p90 của video mẫu.

## 4. Công thức các kiểu move

| Move | Cách đặt key |
| --- | --- |
| **Push-in vào toà nhà/dự án** | key trước: toàn cảnh, z ≈ 0; key tới: `look(d_toà_nhà, ...)`, z +300…+400, orbit +2…+4°. Nhãn giá nổi lên ở 70–85% quãng đường. |
| **Truck ngang skyline** | x tăng đều qua 2–3 key, y gần như giữ; đặt 1 vật tiền cảnh (depth −300…−450) cắt ngang khung giữa đường để parallax rõ. |
| **Crane lên lộ toàn cảnh** | y từ +250 về −100, tilt +3° → 0, z lùi −100; dùng cho hook hoặc kết. |
| **Bay xuyên mây/tiền cảnh** | lớp mây depth −150…−250; z vượt `P + d − 0,3P` → lớp mờ đi khi camera xuyên qua; lớp sau lộ ra. |
| **Orbit quanh mô hình dự án** | orbit −5° → +5° trong 5–8 s, x bù nhẹ để vật thể giữ giữa khung. |
| **Đi dọc biểu đồ** | biểu đồ ở depth 0; camera x chạy từ đầu tới cuối đường giá trong lúc `strokeDashoffset` vẽ ra, cùng thời lượng, để "ngòi bút" luôn gần giữa khung. Số cuối nổi lên khi camera tới đỉnh. |
| **Dive vào bản đồ** | bản đồ thật dựng sẵn thành video bằng `scripts/bake-basemap.mjs` của `/hyperframes` (take riêng); ghim/nhãn vẽ SVG phía trên; nối với take thành phố bằng match-move theo z. |
| **Kéo lùi kết** | z về −200…−300, orbit nhẹ ngược chiều trước đó; câu kết HUD đáp và đứng yên tới hết. |

## 5. Tài sản (ảnh tách lớp)

- **Nguồn:** ảnh flycam, ảnh/phối cảnh dự án, ảnh đường phố có quyền dùng; hoặc minh hoạ vector vẽ theo lớp. Ảnh nơi thật thì dùng ảnh thật, không vẽ lại.
- **Tách lớp:** Photoshop (Select Subject/Sky), `rembg`, hoặc bản đồ độ sâu (Depth Anything) rồi cắt theo ngưỡng thành 3–5 PNG nền trong suốt. **Vá phần nền** phía sau mỗi lớp trước (content-aware/generative fill), nếu không camera trượt sẽ lộ lỗ.
- **Độ phân giải cần có:** ảnh ở lớp `d` hiện lớn tới `(P+d)/(P+d−z_max)` lần kích thước thiết kế. Ví dụ depth 0, z_max = 400 → 1,67×: khung 1920 cần ảnh ≥ 3200 px. Ảnh rất rộng (skyline dài) cắt thành các ô ≤ 8000 px.
- **Phủ đủ:** mỗi lớp rộng hơn vùng camera quét + 30–50% dự phòng cho dolly lùi/orbit/float; lớp trời và đất kéo dài thoải mái.
- **Đặt ảnh:** `<img src="assets/...">` (không có `/` ở đầu) đặt `position:absolute` trong `.w-layer`, toạ độ theo khung thiết kế của lớp. Ảnh không cần `class="clip"` — nó sống suốt take.
- **Phối cảnh khí quyển:** lớp càng xa càng sáng, ít tương phản, ngả màu trời (thêm một lớp sương mỏng 15–25% opacity giữa xa và giữa). Đây là thứ làm parallax "đọc" được.

Độ sâu gợi ý: trời 2500–4000 · skyline xa 1500–2000 · sương 1200–1400 · khối giữa 700–1000 · vật thể chính 200–400 · mặt phẳng số liệu 0 · tiền cảnh −250…−450.

## 6. Nối nhiều take (match-move)

Một take = một file scene. Mối nối phải liên tục về chuyển động:

0. **Kiểu chính của video mẫu: zoom-blur xuyên tâm.** Dùng shader `cinematic-zoom` của `@hyperframes/shader-transitions` (`npx hyperframes catalog --tag transition --json`), đặt đúng lúc cả hai take đang lao vào cùng chiều (take A zoom vào cuối, take B bắt đầu bằng zoom vào). Thời lượng 0,4–0,7 s. Shader chụp cảnh thành texture: snapshot ngay trước/sau mối nối để chắc parallax 3D vẫn hiển thị đúng. Khoảng 1 lần mỗi 8–15 s (`style-mau.md`).
1. **Cùng vận tốc:** key cuối take A đặt `carry: true` (giữ nguyên vận tốc, không đáp), key đầu take B mặc định đã đang chạy; chỉnh để tốc độ trên màn hình và hướng hai bên khớp nhau (đo bằng `analyze_refs.py`: cột "Vào/ra khi đang chạy", `dir_out`/`dir_in`).
2. **Che mối nối bằng vật thể:**
   - *Foreground wipe:* một cột/toà nhà tiền cảnh lướt qua che kín khung; cắt đúng lúc che kín; take B mở ra bằng một vật tiền cảnh cùng màu đang lướt đi cùng hướng.
   - *Zoom xuyên:* take A dive vào cửa sổ/màn hình/ô bản đồ đến khi màu của nó lấp khung; take B bắt đầu từ chính màu đó và lùi ra.
   - *Whip:* lướt nhanh 0,2–0,3 s có motion blur ngang, hai bên cùng hướng.
3. Không crossfade giữa hai thế giới; hard cut thuần ≤ 1/3 số mối nối.

Rig hiện chạy cả take từ một đồng hồ; khi tách take, sao chép file scene (`dive.html` / `world.html`), đổi id scene (`data-composition-id`, host id, khoá `window.__timelines`) và tiền tố id phần tử cho duy nhất.

## 7. Lỗi thường gặp

| Triệu chứng | Nguyên nhân / cách sửa |
| --- | --- |
| Hết parallax, mọi lớp trôi như một tấm | Có `opacity<1`, `filter`, `overflow:hidden`, `clip-path`, `mix-blend-mode` trên `#w-stage`/`#w-cam` → Chrome làm phẳng 3D. Đưa hiệu ứng xuống từng lớp con. |
| `check` báo `dead_stretch` khi camera đang chạy | `data-layout-ignore` trên `#w-stage`/`#w-cam`; dùng `data-layout-allow-overflow`/`-overlap` thay thế. |
| Một lớp phóng to khổng lồ rồi lật ngược | z vượt quá `P + d`; rig đã làm mờ ở 0,3P→0,12P, nhưng hãy đặt key để không vượt. |
| Lộ mép lớp khi kéo lùi/orbit | lớp chưa đủ rộng; mở rộng 30–50% và snapshot ở các key cực trị. |
| Chữ trong thế giới bị nhoè | chữ bị phóng > 1,3× do dolly; thiết kế ở kích thước cuối, hoặc chuyển sang HUD/depth 0. |
| Giật ở mốc key | hai key quá gần với vận tốc khác nhau; giãn key ≥ 2 s hoặc bỏ key thừa. |
| Render khác preview | có `Math.random`/`Date.now`/`requestAnimationFrame`; mọi thứ phải là hàm của `clock.t`. |
| Motion blur (`data-motion-blur`) làm mất 3D | blur dùng filter trên phần tử; chỉ bật sau khi snapshot xác nhận parallax còn nguyên. |

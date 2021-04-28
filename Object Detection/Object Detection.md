# **R-CNN**

## Classification
single object에 대해서 object의 클래스를 분류하는 문제


## Classification + Localization
single object에 대해서 object의 위치를 bounding box로 찾고 클래스를 분류하는 문제


## Object Detection
multiple objects에서 각각의 object에 대해 classification + localization을 수행하는 것


## Instance Segmentation
object detection과 유사하지만, 다른 점은 object의 위치를 bounding box가 아닌 실제 edge로 찾는 것

---
## Object Detection

### 2-Stage detector
selective search, region proposal network등을 통해 object가 있을만한 영역을 뽑아낸다. 이 영역을 RoI(Region of Interest)라고 한다. 이런 영역들을 뽑아내고 나면 각 영역들을 convolution network를 통해 classification, box regression(localization)을 수행한다.


### 1-Stage detector
RoI영역을 먼저 추출하지 않고 전체 image에 대해서 convolution network로 classification, box regression(locaization)을 수행한다. 여러 noise, 즉 여러 object가 섞여있는 전체 image에서 이를 수행하는 것이 특정 object 하나만 담고 있을 때보다 정확도는 더 떨어진다. 그러나 속도가 빠르다는 장점이 있다.


---
## R-CNN
Image Classification을 수행하는 CNN과 localization을 위한 regional proposal알고리즘을 연결한 모델

### R-CNN Process
1. Image 입력
2. Selective search 알고리즘에 의해 regional proposal output 약 2000개를 추출
    2-1. 추출한 regional proposal output을 모두 동일 input size로 만들어주기 위해 warp해준다.
3. 2000개의 warped image를 각각 CNN 모델에 넣는다.
4. 각각의 convolution 결과에 대해 classifiction을 진행해 결과를 얻는다.


### 1. Region Proposal(영역 찾기)
: object가 있을법한 영역을 찾는 모듈(기존의 sliding window 방식의 비효율성 극복)

R-CNN에서는 가장 먼저 region proposal 단계에서 "물체가 있을 법한 영역"을 찾는다. 기존의 sliding window 방식은 이미지에서 물체를 찾기 위해 window의 크기와 비율을 임의로 바꿔가며 모든 영역에 대해 탐색하는 것이다. 그러나 이렇게 임의의 크기, 비율로 모든 영역을 탐색하는 것은 매우 느리다. R-CNN에서는 이 비효율성을 극복하기 위해 Selective search 알고리즘을 사용한다.  
- selective search 알고리즘을 통해 색상, 질감, 영역 크기 등을 이용해 non-object-based segmentation을 수행한다. 이 작업을 통해 많은 small segemented areas들을 얻을 수 있다.  
- Bottom-up 방식으로 small segmented areas들을 합쳐 더 큰 segmented areas들을 만든다.  
- 바로 위 작업을 반복하여 최종적으로 2000개의 region proposal을 생성한다.  
selective search 알고리즘에 의해 2000의 region proposal이 생성되면 이들을 모두 CNN에 넣기 전에 같은 사이즈로 warp시켜야 한다.

### 2. CNN
: 각각의 영역으로부터 고정된 크기의 Feature Vector를 뽑아낸다  

Warp 작업을 통해 region proposal 모두 224x224 크기가 되면 CNN모델에 넣는다. 여기서 CNN은 AlexNet의 구조를 거의 그대로 가져다 사용한다. 최종적으로 CNN을 거쳐 각각의 region proposal로부터 4096-dimentional feature vector를 뽑아내고, 이를 통해 고정 길이의 feature vector를 만들어낸다.

### 3. SVM
classification을 위한 선형 지도 학습 모델
- classifier로 softmax 사용하지 않고 SVM 사용한 이유? : CNN fine-tuning 위한 학습 데이터가 시기상 많지 않아 softmax 적용시키면 오히려 성능이 낮아지기 때문  
CNN모델로부터 feature가 추출되면 Linear SVM을 통해 classification을 진행한다.  
SVM은 CNN으로부터 추출된 각각의 feature vector들의 점수를 class별로 매기고, 객체인지 아닌지, 객체라면 어떤 객체인지 판별하는 classifier다.


#### 3-1. Bounding Box Regression
Selective search로 만든 bounding box는 정확하지 않기 때문에 물체를 정확히 감싸도록 조정해주는 bounding box regression(선형회귀 모델)이 존재한다.

---
### Summary
**R-CNN의 과정**
1. R-CNN은 selective search를 통해 region proposal을 먼저 뽑아낸 후 CNN모델에 들어간다.
2. Localization error를 줄이기 위해 CNN feature를 이용해 bounding box regression model을 수정한다.

**단점**
1. selective search로 2000개의 region proposal을 뽑고 각 영역마다 CNN을 수행하기 때문에 CNN연산 * 2000 만큼의 시간이 소요된다.
2. CNN, SVM, Bounding Box Regression 총 세가지의 모델이 multi-stage pipeline로 한 번에 학습되지 않는다.  
각 region proposal에 대해 convNet forward pass를 실행할 때 연산을 공유하지 않기에 end-to-end로 학습 불가능. 따라서 SVM, bounding box regression에서 학습한 결과가 CNN을 업데이트 시키지 못함.


이 두가지 문제를 RoI pooling으로 해결한 것이 Fast R-CNN!!



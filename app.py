
---
title: "Prediksi Variabel 'classe' Menggunakan Random Forest"
author: "Fadhilah Nurjannah"
output: html_document
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
library(caret)
library(rpart)
library(randomForest)
library(dplyr)
```

## 1. Tujuan

Tujuan proyek ini adalah memprediksi gerakan aktivitas fisik berdasarkan sinyal dari sensor menggunakan model machine learning, dengan target variabel `classe`.

## 2. Import dan Pra-pemrosesan Data

```{r load-data}
train_raw <- read.csv("pml-training.csv", na.strings = c("NA", "", "#DIV/0!"))
test_raw <- read.csv("pml-testing.csv", na.strings = c("NA", "", "#DIV/0!"))
```

```{r preprocessing}
# Menghapus kolom dengan banyak NA
train_clean <- train_raw[, colMeans(is.na(train_raw)) < 0.9]
# Hapus kolom yang tidak relevan (kolom awal seperti nama, waktu, dll)
train_clean <- train_clean[, -c(1:7)]

# Split data training/validasi
set.seed(123)
inTrain <- createDataPartition(train_clean$classe, p = 0.7, list = FALSE)
training <- train_clean[inTrain, ]
validation <- train_clean[-inTrain, ]
```

## 3. Pembangunan Model

```{r model}
set.seed(123)
model_rf <- randomForest(classe ~ ., data = training, ntree = 100)
```

## 4. Evaluasi Model

```{r evaluate}
pred_val <- predict(model_rf, newdata = validation)
confusionMatrix(pred_val, validation$classe)
```

## 5. Prediksi Kasus Uji

```{r predict-test}
# Menyesuaikan kolom test set agar cocok dengan training set
test_clean <- test_raw[, colnames(test_raw) %in% colnames(training)]
# Hapus variabel target jika ada
test_clean <- test_clean[, -which(names(test_clean) == "classe")]
# Prediksi
pred_test <- predict(model_rf, test_clean)
pred_test
```

## 6. Kesimpulan

Model Random Forest memiliki akurasi tinggi dalam memprediksi kelas gerakan berdasarkan data sensor. Proses pra-pemrosesan seperti penghapusan missing values dan fitur tidak relevan sangat berpengaruh terhadap hasil prediksi.

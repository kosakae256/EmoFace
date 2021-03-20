#include <mutex>
#include <thread>
#include <iostream>
#include <fstream>
#include <time.h>
#include <string.h>
#ifdef _MSC_VER
#include <windows.h>
#else
#include <unistd.h>
#endif
#include <sys/timeb.h>
#include <condition_variable>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>

#include <queue>
std::queue<cv::Mat*> _frameQueue;
std::mutex _mutex;

#include "st_sensight_sdk.h"

using namespace std;

#define FRAME_SIZE_720  1280 * 720 * 3 / 2

#ifdef _MSC_VER
#define strcasecmp _stricmp
#endif

cv::VideoCapture cap;

volatile bool sFrameTrackerStop;

// 顔情報をアップデート
void updateCurrentFaces(cv::Mat* frame) {
	// 画像中に映っている顔の情報
	STICurrentFaces* faces;
	STIResult ret = STGetCurrentFaces(&faces);

	if (ret == STI_OK) {
		// 顔の属性
		STIFaceAttribute basicAttribute;
		// 顔の表情
		STIFaceEmotion faceEmotion;
		// 顔のスマイル度
		STIFaceSmile faceSmile;

		// 顔の個数
		int faceCount = faces->faceCount;

		if (faceCount > 0) {
			// 顔の情報
			STITrackFace* face = &(faces->faces[0]);

			int gender = face->basicAttribute.gender;
			// 男性(0)でもなく、女性(1)でもないなら、性別を男性(0)に
			if (gender != 0 && gender != 1) {
				gender = 0;
			}

			cout << "--- RESULTS START ---\n";

			// 顔の属性
			cout << "image_quality: " << face->faceImageQuality << "\n";
			cout << "age: " << face->basicAttribute.age << "\n";
			cout << "gender: " << gender << "\n";
			cout << "is_mask: " << face->basicAttribute.mask << "\n";
			cout << "glasses: " << face->basicAttribute.glasses << "\n";
			cout << "is_beard: " << face->basicAttribute.beard << "\n";
			cout << "charm_score: " << face->basicAttribute.charmScore << "\n";
			cout << "other_count: " << face->basicAttribute.otherCount << "\n";

			// 顔の表情
			cout << "is_positive: " << face->faceEmotion.positive << "\n";
			cout << "is_neutral: " << face->faceEmotion.neutral << "\n";
			cout << "is_negative: " << face->faceEmotion.negative << "\n";

			// 顔のスマイル度
			cout << "smile_score: " << face->faceSmile.currentSmileScore << "\n";
			cout << "average_smile_score: " << face->faceSmile.averageSmileScore << "\n";

			cout << "--- RESULTS END ---\n";
		}
	}
	else {
		cout << "[ERROR] Model failed getting current faces.\n";
	}
}

// レンダリング
void frameTracker() {
	static int count = 0;

	cv::Mat srcFrame;
	STIImage image = { 0 };
	STIResult ret = STI_OK;

	while (!sFrameTrackerStop) {
		cap >> srcFrame;

		if (srcFrame.empty()) {
			if (count++ >= 10) {
				exit(1);
			}

			cout << "[ERROR] Black frame grabbed.\n";

#ifdef _MSC_VER
			Sleep(30);
#else
			usleep(30 * 1000);
#endif
			continue;
		}
		else {
			count = 0;
		}

		cv::Mat dstFrame = srcFrame;

		{
			std::unique_lock<std::mutex> locker(_mutex);
			cv::Mat* copy = new cv::Mat();
			dstFrame.copyTo(*copy);
			_frameQueue.push(copy);
		}

		image.data = dstFrame.data;
		image.format = STI_PIX_FMT_BGR888;
		image.width = dstFrame.cols;
		image.height = dstFrame.rows;
		image.stride = dstFrame.cols * 3;
		image.reserved0 = 0;
		image.reserved1 = 0;

		ret = STTrackAsync(&image);
		if (ret != STI_OK) {
			cout << "[ERROR] Async track failed, rc = " << ret << "\n";
		}

#ifdef _MSC_VER
		Sleep(30);
#else
		usleep(30 * 1000);
#endif
	}
}

// フレーム取得
void loggerThread() {
	while (!sFrameTrackerStop) {
		{
			std::unique_lock<std::mutex> locker(_mutex);
			if (_frameQueue.empty() == false) {
				// フレームを取得
				cv::Mat* frame = _frameQueue.front();
				_frameQueue.pop();

				// フレームを更新
				updateCurrentFaces(frame);

				resize(*frame, *frame, cv::Size(), 0.5, 0.5);

				// フレームを開放
				delete frame;
			}
		}

#ifdef _MSC_VER
		Sleep(10);
#else
		usleep(30 * 1000);
#endif
	}
}

int main(int argc, char* argv[]) {
	// コマンドライン引数が指定されていないなら
	if (argc == 1) {
		// カメラを起動
		cap.open(0);
	} else {
		// 動画をロード
		string filePath = argv[1];
		cap.open(filePath);
	}

	// カメラもしくは動画の解像度を設定
	cap.set(cv::VideoCaptureProperties::CAP_PROP_FRAME_HEIGHT, 720);
	cap.set(cv::VideoCaptureProperties::CAP_PROP_FRAME_WIDTH, 1280);

	// カメラもしくは動画の読み込みが失敗したら
	if (!cap.isOpened()) {
		cout << "[ERROR] Openning capture failed.\n";
		return -1;
	}

	// コンフィグのパス
	const char* configFilePath = "config\\device.cfg";
	string modelDir = "primary_models\\";
	const char* licensePath = "primary_models\\license.lic";
	const char* activationCodePath = "primary_models\\code.dat";

	// モデルをロード
	STIResult ret = STSdkInit(STI_SOFTWARE_MODE, licensePath, activationCodePath, (const char*)configFilePath);
	STSetModelPath(STI_MODEL_FACE_DETECT, (modelDir + "M_Detect_Hunter_Common_Gray_10.1.1.model").c_str());
	STSetModelPath(STI_MODEL_FACE_ALIGN, (modelDir + "M_Align_Deepface_106_track_2.20.1.model").c_str());
	STSetModelPath(STI_MODEL_FACE_HEADPOSE, (modelDir + "M_Align_CalcPose_Ann_106_2.3.0.model").c_str());
	STSetModelPath(STI_MODEL_FACE_ATTR, (modelDir + "M_Attribute_Face_Advertisement_2.11.1.model").c_str());
	STSetModelPath(STI_MODEL_FACE_VERIFY, (modelDir + "M_Verify_Insight_Common_4.2.0.model").c_str());
	STSetModelPath(STI_MODEL_BODY_DETECT, (modelDir + "M_Detect_Body_Hunter_1.7.0.model").c_str());
	STSetModelPath(STI_MODEL_BODY_ALIGN, (modelDir + "M_Detect_Body_Keypoints_5.0.17.model").c_str());
	STSetModelPath(STI_MODEL_BODY_ATTR, (modelDir + "M_Attribute_Body_Fir_1.2.2.model").c_str());

	// モデルをチェック
	if (ret != STI_OK) {
		cout << "[ERROR] Model init failed.\n";
		return -1;
	}

	STSetEnableWatch(1);

	ret = STSdkStart();
	if (ret != STI_OK) {
		cout << "[ERROR] Startting model failed.\n";
		return -1;
	}

	// ロガーを使用
	std::thread logger_thread;
	logger_thread = thread(loggerThread);

	// レンダーを使用
	frameTracker();

	ret = STSdkStop();
	if (ret != STI_OK) {
		cout << "[ERROR] Stopping model failed.\n";
	}

	return 0;
}
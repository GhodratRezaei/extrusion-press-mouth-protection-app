#include "mainwindow.h"
#include <QApplication>
#include <QLocale>
#include <QTranslator>


// // // // To test the video streamig
// #include <QLabel>
// #include <QPixmap>
// #include <opencv2/opencv.hpp>



// QPixmap cvMatToQPixmap(const cv::Mat& mat) {
//     // Convert the OpenCV image to QImage
//     QImage img(mat.data, mat.cols, mat.rows, mat.step, QImage::Format_RGB888);
//     // Convert the QImage to QPixmap
//     return QPixmap::fromImage(img.rgbSwapped());
// }


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    QTranslator translator;
    const QStringList uiLanguages = QLocale::system().uiLanguages();
    for (const QString &locale : uiLanguages) {
        const QString baseName = "qt_" + QLocale(locale).name();
        if (translator.load(":/i18n/" + baseName)) {
            a.installTranslator(&translator);
            break;
        }
    }


    
    // // // Video Streamer
    // // Load image using OpenCV
    // cv::Mat img = cv::imread(":/images/logo.jpg", cv::IMREAD_COLOR);
    // if (img.empty()) {
    //     qWarning("Could not open or find the image.");
    //     return -1;
    // }

    // // Create a QLabel and set the pixmap
    // QLabel label;
    // label.setPixmap(cvMatToQPixmap(img));
    // label.show();




    MainWindow w;
    w.show();
    return a.exec();
}




#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QPixmap>  // Include QPixmap header




using namespace cv;



MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    // Set the window icon
    QIcon icon(":/images/favicon.ico");
    this->setWindowIcon(icon);


    // Load the image from resources
    QPixmap image(":/images/logo.jpg");  // ":/images/your_image.png" should match your resource path
    // QPixmap video_image(":/images/logo.jpg")

    // Resize the image to the specified width and height
    QPixmap scaledImage = image.scaled(141, 83, Qt::IgnoreAspectRatio, Qt::SmoothTransformation);
    // QPixmap video_scaledImage = video_image.scaled(141, 83, Qt::IgnoreAspectRatio, Qt::SmoothTransformation);

    // Load the scaled image to the danilei_label widg et
    if (scaledImage.isNull()){
        qDebug() << "Failed to load image";
    }else{
        qDebug() << "Image loaded successfully";
        ui->danieli_label->setPixmap(scaledImage);
    }

    // openCV Implementation
    qDebug() << "OpenCV version is: " << CV_VERSION;

    // // Video Streamer
    // Load image using OpenCV
    cv::Mat img = cv::imread(":/images/logo.jpg");
    // if (img.empty()) {
    //     qWarning("Could not open or find the image.");
    //     return -1;
    // }

    // // Create a QLabel and set the pixmap
    // QLabel label;
    // label.setPixmap(cvMatToQPixmap(img));
    // label.show();


}

MainWindow::~MainWindow()
{
    delete ui;
}

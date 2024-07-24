#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QPixmap>  // Include QPixmap header


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);




    // Load the image from resources
    QPixmap image(":/images/logo.jpg");  // ":/images/your_image.png" should match your resource path

    // Resize the image to the specified width and height
    QPixmap scaledImage = image.scaled(141, 83, Qt::IgnoreAspectRatio, Qt::SmoothTransformation);

    // Load the scaled image to the danilei_label widget
    if (scaledImage.isNull()){
        qDebug() << "Failed to load image";
    }else{
        qDebug() << "Image loaded successfully";
        ui->danieli_label->setPixmap(scaledImage);

    }




}

MainWindow::~MainWindow()
{
    delete ui;
}

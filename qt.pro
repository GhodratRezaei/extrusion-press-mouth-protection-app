QT += core gui widgets

CONFIG += c++17

# Include path to OpenCV headers
INCLUDEPATH += C:/opencv/build/include

# OpenCV Libraries
LIBS += -LC:/opencv/build/x64/vc16/lib

# Use separate libraries for debug and release builds
CONFIG(release, debug|release): LIBS += -lopencv_world4100
CONFIG(debug, debug|release): LIBS += -lopencv_world4100d



SOURCES += \
    main.cpp \
    mainwindow.cpp

HEADERS += \
    mainwindow.h

FORMS += \
    mainwindow.ui

TRANSLATIONS += \
    qt_en_GB.ts
CONFIG += lrelease
CONFIG += embed_translations

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

RESOURCES += Resources/resources.qrc \
    resources.qrc



win32:CONFIG(release, debug|release): LIBS += -LC:/opencv/build/x64/vc16/lib/ -lopencv_world4100
else:win32:CONFIG(debug, debug|release): LIBS += -LC:/opencv/build/x64/vc16/lib/ -lopencv_world4100d

INCLUDEPATH += C:/opencv/build/include
DEPENDPATH += C:/opencv/build/include

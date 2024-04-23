package main

import (
    "database/sql"
    "fmt"
    "image"
    "image/color"
    "io/ioutil"
    "log"
    "math/rand"
    "os"
    "strconv"
    "time"

    _ "github.com/lib/pq"
    "github.com/twinj/uuid"
    "gocv.io/x/gocv"
)

var (
    connStr = "user=root dbname=photos password=root host=postgres port=5432 sslmode=disable"
)

func createTable() error {
    db, err := sql.Open("postgres", connStr)
    if err != nil {
        return err
    }
    defer db.Close()

    _, err = db.Exec(`CREATE TABLE IF NOT EXISTS cartoon(
        photoID SERIAL PRIMARY KEY,
        name TEXT,
        photoImg BYTEA
    )`)
    if err != nil {
        return err
    }

    return nil
}

func writeBlob(photoID int, filePath, name string) error {
    db, err := sql.Open("postgres", connStr)
    if err != nil {
        return err
    }
    defer db.Close()

    drawing, err := ioutil.ReadFile(filePath)
    if err != nil {
        return err
    }

    _, err = db.Exec(`INSERT INTO cartoon(photoID, name, photoImg) VALUES($1, $2, $3)`,
        photoID, name, drawing)
    if err != nil {
        return err
    }

    return nil
}

func main() {
    if err := createTable(); err != nil {
        log.Fatalf("Error creating table: %v", err)
    }

    cam, err := gocv.VideoCapture("/dev/video0")
    if err != nil {
        log.Fatalf("Error opening camera device: %v", err)
    }
    defer cam.Close()

    frame := gocv.NewMat()
    defer frame.Close()

    for {
        if ok := cam.Read(&frame); !ok {
            log.Fatalf("Error reading frame from camera")
        }

        frame1 := frame.Clone()
        frame2 := frame.Clone()

        gocv.AbsDiff(frame1, frame2, &frame1)

        gray := gocv.NewMat()
        defer gray.Close()
        gocv.CvtColor(frame1, &gray, gocv.ColorBGRToGray)

        blur := gocv.NewMat()
        defer blur.Close()
        gocv.GaussianBlur(gray, &blur, image.Point{X: 5, Y: 5}, 0)

        _, thresh := gocv.Threshold(blur, 20, 255, gocv.ThresholdBinary)
        dilated := gocv.NewMat()
        defer dilated.Close()
        kernel := gocv.GetStructuringElement(gocv.MorphRect, image.Point{X: 3, Y: 3})
        gocv.Dilate(thresh, &dilated, kernel)

        contours := gocv.FindContours(dilated, gocv.RetrievalExternal, gocv.ChainApproxSimple)
        for _, c := range contours {
            if area := gocv.ContourArea(c); area < 5000 {
                continue
            }

            rect := gocv.BoundingRect(c)
            gocv.Rectangle(&frame1, rect, color.RGBA{0, 255, 0, 0}, 2)

            fmt.Println("t")

            start := time.Now()
            photoTime := 4
            for time.Since(start).Seconds() <= float64(photoTime) {
                _, photo := cam.Read()

                myUUID := uuid.NewV4().String()
                gocv.IMWrite(fmt.Sprintf("./photos/%s.jpg", myUUID), photo)

                integer := rand.Intn(11)
                writeBlob(integer, fmt.Sprintf("./photos/%s.jpg", myUUID), myUUID)

                fmt.Println(myUUID)
                time.Sleep(4 * time.Second)
            }
        }
    }
}

import Image
import numpy as np
import glob

def createImage(v, filename,imsize):
    v.shape = (-1,) #change to 1 dim array
    a, b = v.min(), v.max()
    im = Image.new('L', imsize)
    scaledarray = ((v-a)* 255/(b - a))
    im.putdata(scaledarray)
    im.save(filename)


########## PREPROCESSING ##########

face_vectors = []
for file in glob.glob("data/meyer_e*.jpg"):
    unprocessed_face = Image.open(file)

    # Convert to monochrome, which allows for a 2D matrix with black/white values rather than RGB
    unprocessed_face = unprocessed_face.convert('L')
    pixel_matrix = np.array(unprocessed_face) # 2D matrix of pixel intensities

    # Unroll the matrix into a 1D vector for feeding into eigenface algorithm
    face_vectors.append(pixel_matrix.ravel())


########## EIGENFACE ALGORITHM ##########

# Create a 5 x 57,600-dimensional matrix containing pixel values from the images above
faces = np.array(face_vectors)

# Compute a matrix of elementwise average pixel values for mean centering the pixel matrix
# This is an important step in PCA, as seen in step 2 here: http://en.wikipedia.org/wiki/Eigenface
# And here: http://en.wikipedia.org/wiki/Principal_component_analysis#Discussion
average = np.average(faces, axis=0)
centered_faces = faces - average

# PCA can be performed in several ways, one of which tries to calculate the eigenvectors of a
# covariance matrix, which is described more fully here: http://en.wikipedia.org/wiki/Covariance_matrix
# This creates a covariance matrix based on the mean-centered faces calculated above.
covariance = np.dot(centered_faces, centered_faces.transpose())

# Gets eigenvectors and eigenvalues of covariance matrix. This is basically the PCA step.
# More info on that here: http://en.wikipedia.org/wiki/Eigenvalue,_eigenvector_and_eigenspace
evals, evects = np.linalg.eig(covariance)

# Sort the principal components abd prep them for image generation
reverse_evals = evals.argsort()[::-1]
sorted_evects = evects[:, reversed_evals]
sorted_evects = sorted_evects.transpose()

# Loop through and produce images. 0 corresponds to the first principal component, 1 to the second, etc.
for i in range(len(sorted_evects)):
    face = np.dot(sorted_evects[i], centered_faces)
    createImage(face, "eigenphil%s.jpg" % i,(240,240))